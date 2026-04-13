from sentence_transformers import SentenceTransformer
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the embedding model (using a lightweight model for faster inference)
# Models available: https://www.sbert.net/docs/pretrained_models.html
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast and lightweight model

try:
    embedding_model = SentenceTransformer(MODEL_NAME)
    logger.info(f"Embedding model '{MODEL_NAME}' loaded successfully")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    embedding_model = None


def create_embedding(text: str) -> List[float]:
    """
    Create an embedding vector for the given text.
    
    Args:
        text: The text to embed
        
    Returns:
        List of floats representing the embedding vector
        
    Raises:
        ValueError: If the embedding model is not initialized or text is empty
    """
    if not embedding_model:
        raise ValueError("Embedding model not initialized")
    
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Generate embedding
    embedding = embedding_model.encode(text.strip())
    
    # Convert numpy array to list of floats
    return embedding.tolist()


def get_embedding_dimension() -> int:
    """
    Get the dimension of the embedding vectors.
    
    Returns:
        The dimension of the embedding vectors
    """
    if not embedding_model:
        raise ValueError("Embedding model not initialized")
    
    return embedding_model.get_sentence_embedding_dimension()
