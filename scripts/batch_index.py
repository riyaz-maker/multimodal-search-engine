# scripts/batch_index.py

import os
import logging
import numpy as np
import psycopg2
from dotenv import load_dotenv
from pinecone import Pinecone
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm.auto import tqdm

from src.core.embedding import EmbeddingModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BatchIndexer:
    def __init__(self, batch_size=64):
        load_dotenv()
        self.batch_size = batch_size
        self.embedder = EmbeddingModel()
        self._init_db_clients()

    def _init_db_clients(self):
        try:
            self.pg_conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.es_client = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))

            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            self.pinecone_index = pc.Index("multimodal-search")
            logger.info("All database and index clients initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize clients: {e}")
            raise

    def _fetch_products_from_db(self):
        logger.info("Fetching product data from PostgreSQL...")
        with self.pg_conn.cursor() as cursor:
            cursor.execute("SELECT article_id, prod_name, cleaned_description, image_path, product_group_name, colour_group_name, section_name FROM products")
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        logger.info(f"Fetched {len(products)} products.")
        return [dict(zip(columns, row)) for row in products]

    def run(self):
        products = self._fetch_products_from_db()

        for i in tqdm(range(0, len(products), self.batch_size), desc="Indexing Batches"):
            batch = products[i:i + self.batch_size]
            es_actions = []
            pinecone_vectors = []

            for product in batch:
                # Generate embeddings
                text_emb = self.embedder.embed_text(product['cleaned_description'])
                image_emb = self.embedder.embed_image(product['image_path'])

                # Skip product if embeddings could not be generated
                if text_emb is None or image_emb is None:
                    logger.warning(f"Skipping article_id {product['article_id']} due to missing embedding.")
                    continue

                # Combine embeddings
                combined_emb = np.mean([text_emb, image_emb], axis=0).tolist()

                # Prepare data for Elasticsearch (metadata)
                es_actions.append({
                    "_index": "products_metadata",
                    "_id": product['article_id'],
                    "_source": {
                        "article_id": product['article_id'],
                        "prod_name": product['prod_name'],
                        "product_group_name": product['product_group_name'],
                        "colour_group_name": product['colour_group_name'],
                        "section_name": product['section_name'],
                    }
                })

                # Prepare data for Pinecone (vector + article_id)
                pinecone_vectors.append({
                    "id": product['article_id'],
                    "values": combined_emb
                })

            # Perform bulk operations if there's anything to process
            if es_actions:
                bulk(self.es_client, es_actions)
            if pinecone_vectors:
                self.pinecone_index.upsert(vectors=pinecone_vectors)

        logger.info("Batch indexing pipeline completed successfully.")
        self.pg_conn.close()

if __name__ == "__main__":
    indexer = BatchIndexer()
    indexer.run()