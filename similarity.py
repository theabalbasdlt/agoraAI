from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def compute_cosine_similarity(user_embedding: List[float], event_embedding: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        user_embedding: User profile embedding vector
        event_embedding: Event embedding vector
        
    Returns:
        Cosine similarity score (between -1 and 1, typically 0 to 1 for normalized vectors)
        
    Raises:
        ValueError: If embeddings are not valid or have different dimensions
    """
    if not user_embedding or not event_embedding:
        raise ValueError("Embeddings cannot be empty")
    
    if len(user_embedding) != len(event_embedding):
        raise ValueError(
            f"Embeddings must have the same dimension. "
            f"Got {len(user_embedding)} and {len(event_embedding)}"
        )
    
    try:
        # Convert to numpy arrays
        user_vec = np.array(user_embedding).reshape(1, -1)
        event_vec = np.array(event_embedding).reshape(1, -1)
        
        # Compute cosine similarity
        similarity = cosine_similarity(user_vec, event_vec)[0][0]
        
        # Ensure the result is a float
        return float(similarity)
    except Exception as e:
        raise ValueError(f"Error computing cosine similarity: {str(e)}")


def rank_events_by_similarity(
    user_embedding: List[float],
    event_embeddings: List[Tuple[str, str, str, List[float]]]
) -> List[Tuple[str, str, str, float]]:
    """
    Rank events by their cosine similarity to the user embedding.
    
    Args:
        user_embedding: User profile embedding vector
        event_embeddings: List of tuples (event_id, name, description, embedding)
        
    Returns:
        Sorted list of tuples (event_id, name, description, similarity_score)
        in descending order of similarity
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not user_embedding:
        raise ValueError("User embedding cannot be empty")
    
    if not event_embeddings:
        return []
    
    try:
        # Compute similarities for all events
        similarities = []
        for event_id, name, description, event_embedding in event_embeddings:
            similarity = compute_cosine_similarity(user_embedding, event_embedding)
            similarities.append((event_id, name, description, similarity))
        
        # Sort by similarity score in descending order
        sorted_events = sorted(similarities, key=lambda x: x[3], reverse=True)
        
        return sorted_events
    except Exception as e:
        raise ValueError(f"Error ranking events: {str(e)}")
