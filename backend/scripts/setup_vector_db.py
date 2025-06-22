import os
import logging
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_pinecone():
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in .env file.")

    pc = Pinecone(api_key=api_key)

    index_name = "multimodal-search"

    if index_name in pc.list_indexes().names():
        logging.warning(f"Index '{index_name}' already exists. Skipping creation.")
        return
    try:
        logging.info(f"Creating a new serverless index: '{index_name}'")
        pc.create_index(
            name=index_name,
            dimension=512,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        logging.info(f"Successfully created index '{index_name}'.")

    except Exception as e:
        logging.error(f"Could not create Pinecone index: {e}")
        raise

if __name__ == "__main__":
    setup_pinecone()