import pandas as pd
import numpy as np
import os
import re
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm
import logging
from bs4 import BeautifulSoup

# Configure logging for better visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class HMDataPreparer:
    def __init__(self, base_data_path: str, output_path: str):
        self.base_path = base_data_path
        self.images_base_path = os.path.join(self.base_path, 'images')
        self.articles_path = os.path.join(self.base_path, 'articles.csv')
        self.output_path = output_path
        self.final_csv_path = os.path.join(self.output_path, 'prepared_hm_products.csv')

        os.makedirs(self.output_path, exist_ok=True)
        logger.info(f"Data preparer initialized. Output will be saved to {self.output_path}")

    def _load_and_inspect(self) -> pd.DataFrame:
        logger.info(f"Loading metadata from {self.articles_path}")
        try:
            dtype_map = {
                'article_id': str, 'product_code': str, 'prod_name': 'string',
                'product_type_name': 'category', 'product_group_name': 'category',
                'graphical_appearance_name': 'category', 'colour_group_name': 'category',
                'perceived_colour_value_name': 'category', 'perceived_colour_master_name': 'category',
                'department_name': 'category', 'index_name': 'category', 'index_group_name': 'category',
                'section_name': 'category', 'garment_group_name': 'category', 'detail_desc': 'string'
            }
            df = pd.read_csv(self.articles_path, dtype=dtype_map)
            logger.info("Initial memory usage of loaded data:")
            df.info(memory_usage='deep')
            return df
        except FileNotFoundError:
            logger.error(f"FATAL: The file {self.articles_path} was not found.")
            raise

    @staticmethod
    def _clean_text(text: str) -> str:
        if not isinstance(text, str) or pd.isna(text):
            return ""
        
        text = BeautifulSoup(text, "html.parser").get_text()
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s.,-]', '', text)
        # Consolidate whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _construct_and_verify_image_path(self, article_id: str) -> str | None:
        # H&M image path format: <base>/0<first two digits>/0<full id>.jpg
        sub_dir = f"0{article_id[:2]}"
        image_path = os.path.join(self.images_base_path, sub_dir, f"0{article_id}.jpg")
        
        if not os.path.exists(image_path):
            return None
        
        try:
            with Image.open(image_path) as img:
                img.verify()
                if img.mode != 'RGB':
                    with Image.open(image_path) as img_to_convert:
                         img_to_convert.convert('RGB')
            return image_path
        except Exception:
            return None

    def _process_in_parallel(self, df: pd.DataFrame) -> pd.DataFrame:
        image_paths = [None] * len(df)
        cleaned_descriptions = [None] * len(df)
        
        # Use context manager for the thread pool
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            logger.info(f"Starting parallel processing with {executor._max_workers} workers.")
            
            future_to_idx_img = {
                executor.submit(self._construct_and_verify_image_path, row.article_id): idx 
                for idx, row in df.iterrows()
            }

            for future in tqdm(as_completed(future_to_idx_img), total=len(df), desc="Verifying Images"):
                idx = future_to_idx_img[future]
                image_paths[idx] = future.result()

            descriptions = df['detail_desc'].tolist()
            future_to_idx_text = {
                executor.submit(self._clean_text, desc): i 
                for i, desc in enumerate(descriptions)
            }
            for future in tqdm(as_completed(future_to_idx_text), total=len(descriptions), desc="Cleaning Descriptions"):
                idx = future_to_idx_text[future]
                cleaned_descriptions[idx] = future.result()

        df['image_path'] = image_paths
        df['cleaned_description'] = cleaned_descriptions
        return df

    def run(self):
        """Executes the complete data preparation pipeline."""
        df = self._load_and_inspect()
        
        logger.info("Starting data cleaning and feature engineering.")
        logger.info(f"Initial dataframe shape: {df.shape}")
        
        logger.info(f"Initial missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
        df.dropna(subset=['detail_desc'], inplace=True)
        logger.info(f"Shape after dropping rows with missing descriptions: {df.shape}")

        df = self._process_in_parallel(df)
        
        logger.info("Filtering out products with invalid images or empty descriptions post-cleaning.")
        initial_rows = len(df)
        df.dropna(subset=['image_path'], inplace=True) # Filter out failed image lookups
        df = df[df['cleaned_description'].str.len() > 20] # Keep only reasonably long descriptions
        final_rows = len(df)
        logger.info(f"Dropped {initial_rows - final_rows} rows due to invalid images or short/empty descriptions.")
        
        # Select and reorder columns for a clean, final dataset
        final_columns = [
            'article_id',
            'prod_name',
            'cleaned_description',
            'product_group_name',
            'graphical_appearance_name',
            'colour_group_name',
            'section_name',
            'garment_group_name',
            'image_path'
        ]
        final_columns = [col for col in final_columns if col in df.columns]
        df_final = df[final_columns].copy()
        
        df_final.reset_index(drop=True, inplace=True)
        
        logger.info("Final memory usage of processed data:")
        df_final.info(memory_usage='deep')
        
        logger.info(f"Saving prepared data to {self.final_csv_path}")
        df_final.to_csv(self.final_csv_path, index=False)
        
        logger.info("Data preparation pipeline finished successfully.")
        print(f"\nSuccessfully prepared data for {len(df_final)} products.")
        print(f"Cleaned data saved to: {self.final_csv_path}")
        print("\nFinal DataFrame head:")
        print(df_final.head())


if __name__ == '__main__':
    DATA_DIRECTORY = 'data'
    OUTPUT_DIRECTORY = os.path.join(DATA_DIRECTORY, 'prepared')
    
    # A simple check to guide the user
    if not os.path.exists(os.path.join(DATA_DIRECTORY, 'articles.csv')):
        logger.error("Dataset not found in the 'data/' directory.")
    else:
        preparer = HMDataPreparer(base_data_path=DATA_DIRECTORY, output_path=OUTPUT_DIRECTORY)
        preparer.run()