# src/core/embedding.py

import logging
from sentence_transformers import SentenceTransformer
from PIL import Image
import torch

logger = logging.getLogger(__name__)

class EmbeddingModel:
    def __init__(self, model_name: str = 'clip-ViT-B-32'):
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        try:
            logger.info(f"Loading SentenceTransformer model: {model_name}")
            self.model = SentenceTransformer(model_name, device=self.device)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed_text(self, text: str):
        if not text or not isinstance(text, str):
            return None
        return self.model.encode(text, convert_to_numpy=True, device=self.device)

    def embed_image(self, image_path: str):
        try:
            image = Image.open(image_path)
            return self.model.encode(image, convert_to_numpy=True, device=self.device)
        except FileNotFoundError:
            logger.warning(f"Image not found at path: {image_path}")
            return None
        except Exception as e:
            logger.error(f"Could not process image {image_path}: {e}")
            return None