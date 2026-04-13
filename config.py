"""
Configuration settings for the Embeddings API
"""

# Server Configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8000
DEBUG = False

# Embedding Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight model, good balance of speed and quality
# Other options:
# - "sentence-transformers/all-mpnet-base-v2" (larger, slower, more accurate)
# - "sentence-transformers/paraphrase-MiniLM-L6-v2" (good for paraphrases)
# - "sentence-transformers/all-mini-lm-l12-v1" (very fast, smaller dimension)

# API Configuration
API_TITLE = "Embeddings API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API for creating text embeddings and comparing user profiles with events"

# CORS Configuration (for App Inventor)
CORS_ORIGINS = ["*"]  # Allow all origins
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Logging Configuration
LOG_LEVEL = "INFO"

# Similarity Threshold (optional, for filtering)
MIN_SIMILARITY_THRESHOLD = 0.0  # Return all results, no minimum threshold

# Maximum Request Size
MAX_TEXT_LENGTH = 10000  # Maximum characters for text to embed
MAX_EVENTS_PER_REQUEST = 10000  # Maximum events in a comparison request
