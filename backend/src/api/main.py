import os
import io
import logging
from typing import Optional, List, Dict
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import psycopg2
from dotenv import load_dotenv
from pinecone import Pinecone
from elasticsearch import Elasticsearch
from src.core.embedding import EmbeddingModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(title="Multimodal Search API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients for Pinecone, Elasticsearch, and PostgreSQL
try:
    embedder = EmbeddingModel()
    
    # Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    pinecone_index = pc.Index("multimodal-search")

    # Elasticsearch
    es_client = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))

    # PostgreSQL 
    pg_conn = psycopg2.connect(
        host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    logger.info("All clients initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize clients during startup: {e}")
    raise

# Helper Functions
def query_pinecone(query_vector, top_k=20) -> List[str]:
    try:
        results = pinecone_index.query(vector=query_vector, top_k=top_k, include_metadata=False)
        return [match['id'] for match in results['matches']]
    except Exception as e:
        logger.error(f"Pinecone query failed: {e}")
        return []

def query_elasticsearch(text_query, top_k=20) -> List[str]:
    if not text_query:
        return []
    try:
        response = es_client.search(
            index="products_metadata",
            size=top_k,
            query={
                "multi_match": {
                    "query": text_query,
                    "fields": ["prod_name", "product_group_name", "section_name"],
                    "fuzziness": "AUTO"
                }
            }
        )
        return [hit['_id'] for hit in response['hits']['hits']]
    except Exception as e:
        logger.error(f"Elasticsearch query failed: {e}")
        return []

def reciprocal_rank_fusion(ranked_lists: List[List[str]], k=60) -> List[str]:
    scores = {}
    for ranked_list in ranked_lists:
        for i, item_id in enumerate(ranked_list):
            rank = i + 1
            if item_id not in scores:
                scores[item_id] = 0
            scores[item_id] += 1 / (k + rank)
    
    sorted_items = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [item_id for item_id, score in sorted_items]


def fetch_product_details_from_postgres(article_ids: List[str]) -> List[Dict]:
    if not article_ids:
        return []
    
    query = "SELECT article_id, prod_name, cleaned_description, image_path FROM products WHERE article_id = ANY(%s)"
    try:
        with pg_conn.cursor() as cursor:
            cursor.execute(query, (article_ids,))
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            product_map = {str(p[0]): dict(zip(columns, p)) for p in products}
            ordered_products = [product_map[str(aid)] for aid in article_ids if str(aid) in product_map]
            return ordered_products
            
    except Exception as e:
        logger.error(f"PostgreSQL fetch failed: {e}")
        pg_conn.rollback()
        return []

# API endpoint

@app.post("/search/", summary="Perform a multimodal hybrid search")
async def search(
    text_query: Optional[str] = Form(None),
    image_query: Optional[UploadFile] = File(None),
    top_k: int = Form(10)
):
    if not text_query and not image_query:
        raise HTTPException(status_code=400, detail="Provide a text query, an image or both.")

    query_vector = None
    text_emb = embedder.embed_text(text_query) if text_query else None
    
    image_emb = None
    if image_query:
        try:
            image_bytes = await image_query.read()
            image = Image.open(io.BytesIO(image_bytes))
            image_emb = embedder.model.encode(image, convert_to_numpy=True, show_progress_bar=False)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid or corrupt image file: {e}")

    if text_emb is not None and image_emb is not None:
        query_vector = ((0.5 * text_emb) + (0.5 * image_emb)).tolist()
    elif image_emb is not None:
        query_vector = image_emb.tolist()
    else: 
        query_vector = text_emb.tolist()
    
    if query_vector is None:
        raise HTTPException(status_code=500, detail="Could not generate a query vector.")

    pinecone_results = query_pinecone(query_vector, top_k=50)
    es_results = query_elasticsearch(text_query, top_k=50)
    final_ranked_ids = reciprocal_rank_fusion([pinecone_results, es_results])
    final_products = fetch_product_details_from_postgres(final_ranked_ids[:top_k])
    
    return {"results": final_products}