from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List

from models import (
    TextRequest,
    EmbeddingResponse,
    SimilarityRequest,
    SimilarityResponse,
    SimilarEvent
)
from embeddings import create_embedding, get_embedding_dimension
from similarity import rank_events_by_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Embeddings API",
    description="API for creating text embeddings and comparing user profiles with events",
    version="1.0.0"
)

# Add CORS middleware to allow requests from App Inventor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (App Inventor can call from anywhere)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Embeddings API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    try:
        embedding_dim = get_embedding_dimension()
        return {
            "status": "healthy",
            "embedding_dimension": embedding_dim
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {str(e)}"
        )


@app.post("/create-embedding", response_model=EmbeddingResponse, tags=["Embeddings"])
async def create_embedding_endpoint(request: TextRequest):
    """
    Create an embedding vector for the given text.
    
    Args:
        request: Text to embed
        
    Returns:
        Embedding vector and metadata
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        embedding = create_embedding(request.text)
        embedding_dim = get_embedding_dimension()
        
        return EmbeddingResponse(
            text=request.text.strip(),
            embedding=embedding,
            dimension=embedding_dim
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating embedding: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating embedding"
        )


@app.post("/compare-events", response_model=SimilarityResponse, tags=["Similarity"])
async def compare_events(request: SimilarityRequest):
    """
    Compare a user profile embedding with event embeddings and return
    a sorted list of most similar events based on cosine similarity.
    
    Args:
        request: User embedding and list of events with embeddings
        
    Returns:
        Sorted list of events by similarity score (highest first)
    """
    try:
        if not request.user_embedding:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User embedding cannot be empty"
            )
        
        if not request.events:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Events list cannot be empty"
            )
        
        # Prepare event data for ranking
        event_data = [
            (event.event_id, event.name, event.description, event.embedding)
            for event in request.events
        ]
        
        # Rank events by similarity
        ranked_events = rank_events_by_similarity(request.user_embedding, event_data)
        
        # Convert to response format
        similar_events = [
            SimilarEvent(
                event_id=event[0],
                name=event[1],
                description=event[2],
                similarity_score=event[3]
            )
            for event in ranked_events
        ]
        
        return SimilarityResponse(
            similar_events=similar_events,
            count=len(similar_events)
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error comparing events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while comparing events"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
