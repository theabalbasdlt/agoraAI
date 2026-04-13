from pydantic import BaseModel
from typing import List


class TextRequest(BaseModel):
    """Request model for creating embeddings from text"""
    text: str


class EmbeddingResponse(BaseModel):
    """Response model for embeddings"""
    text: str
    embedding: List[float]
    dimension: int


class Event(BaseModel):
    """Model for an event with its embedding"""
    event_id: str
    name: str
    description: str
    embedding: List[float]


class SimilarityRequest(BaseModel):
    """Request model for comparing user profile with events"""
    user_embedding: List[float]
    events: List[Event]


class SimilarEvent(BaseModel):
    """Model for an event with similarity score"""
    event_id: str
    name: str
    description: str
    similarity_score: float


class SimilarityResponse(BaseModel):
    """Response model for similarity results"""
    similar_events: List[SimilarEvent]
    count: int
