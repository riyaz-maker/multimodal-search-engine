import os
import io
import logging
import pandas as pd
import psycopg2
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class PostgresIngestor:
    def __init__(self, csv_path: str, table_name: str):
        load_dotenv()
        self.csv_path = csv_path
        self.table_name = table_name
        self.db_params = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
        if not all(self.db_params.values()):
            raise ValueError("Database configuration error: One or more environment variables are not set in your .env file.")

    def _create_connection(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except psycopg2.OperationalError as e:
            logger.error(f"Could not connect to the PostgreSQL database: {e}")
            logger.error("Please ensure the Docker container is running and the .env file credentials are correct.")
            raise

    def ingest(self, clear_table: bool = True):
        logger.info(f"Starting ingestion of '{self.csv_path}' into table '{self.table_name}'.")

        try:
            df = pd.read_csv(self.csv_path)
            if df.empty:
                logger.warning("Input CSV file is empty. No data to ingest.")
                return
        except FileNotFoundError:
            logger.error(f"The input file was not found at {self.csv_path}")
            raise

        conn = self._create_connection()
        cursor = conn.cursor()

        try:
            if clear_table:
                logger.info(f"Clearing all existing data from table '{self.table_name}' to ensure a clean import.")
                cursor.execute(f"TRUNCATE TABLE {self.table_name} RESTART IDENTITY CASCADE;")

            logger.info(f"Preparing to copy {len(df)} rows into the database via in-memory buffer...")
            
            # Create an in-memory text buffer to stream data efficiently without writing to disk
            buffer = io.StringIO()
            df.to_csv(buffer, index=False, header=False)
            buffer.seek(0) # Rewind the buffer to the beginning for reading
            columns = ','.join(df.columns)
            copy_sql = f"COPY {self.table_name} ({columns}) FROM STDIN WITH (FORMAT CSV)"

            cursor.copy_expert(sql=copy_sql, file=buffer)
            conn.commit()
            
            logger.info(f"Success. Ingested {cursor.rowcount} rows.")

        except (Exception, psycopg2.Error) as e:
            logger.error(f"An error occurred during ingestion: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
            logger.info("Database connection closed.")


if __name__ == '__main__':
    PREPARED_CSV_PATH = 'data/prepared/prepared_hm_products.csv'
    TABLE_NAME = 'products'
    try:
        ingestor = PostgresIngestor(csv_path=PREPARED_CSV_PATH, table_name=TABLE_NAME)
        ingestor.ingest()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")