# Embeddings API for App Inventor

A FastAPI-based service for creating text embeddings and comparing user profiles with events using cosine similarity.

## Features

- **Create Embeddings**: Generate embedding vectors from text
- **Compare Events**: Match a user profile with events and get a ranked list based on similarity
- **Cosine Similarity**: Uses cosine distance for accurate similarity computation
- **CORS Enabled**: Compatible with MIT App Inventor and web applications
- **Fast Inference**: Uses lightweight, efficient embedding model (all-MiniLM-L6-v2)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Verify the Server is Running

Visit: `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

Or check health: `http://localhost:8000/health`

## API Endpoints

### 1. Create Embedding

**Endpoint**: `POST /create-embedding`

**Purpose**: Generate an embedding vector for a given text

**Request Body**:
```json
{
  "text": "Your text here"
}
```

**Response**:
```json
{
  "text": "Your text here",
  "embedding": [0.123, -0.456, 0.789, ...],
  "dimension": 384
}
```

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/create-embedding" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love hiking and outdoor activities"}'
```

---

### 2. Compare Events

**Endpoint**: `POST /compare-events`

**Purpose**: Compare a user's embedding with multiple events and get a sorted list of most similar events

**Request Body**:
```json
{
  "user_embedding": [0.123, -0.456, 0.789, ...],
  "events": [
    {
      "event_id": "event_1",
      "name": "Hiking Trail Adventure",
      "description": "Join us for a challenging hike through mountain trails",
      "embedding": [0.111, -0.444, 0.777, ...]
    },
    {
      "event_id": "event_2",
      "name": "Code Sprint",
      "description": "24-hour programming competition",
      "embedding": [0.999, -0.111, 0.222, ...]
    }
  ]
}
```

**Response**:
```json
{
  "similar_events": [
    {
      "event_id": "event_1",
      "name": "Hiking Trail Adventure",
      "description": "Join us for a challenging hike through mountain trails",
      "similarity_score": 0.856
    },
    {
      "event_id": "event_2",
      "name": "Code Sprint",
      "description": "24-hour programming competition",
      "similarity_score": 0.234
    }
  ],
  "count": 2
}
```

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/compare-events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_embedding": [0.123, -0.456, 0.789],
    "events": [
      {
        "event_id": "e1",
        "name": "Hiking",
        "description": "Mountain trail hiking event",
        "embedding": [0.111, -0.444, 0.777]
      }
    ]
  }'
```

---

## Using with MIT App Inventor

### Step 1: Create Embedding for User Profile

In App Inventor, use the **Web** component:

```
Call Web1.PostText
  url: "http://your-server:8000/create-embedding"
  text: "{"text": "your user profile text"}"
  
When Web1.GotText
  Set user_embedding to call JsonTextDecode(responseContent).embedding
```

### Step 2: Create Event Embeddings

Repeat the above process for each event description to get their embeddings.

### Step 3: Compare and Get Sorted Events

```
Call Web2.PostText
  url: "http://your-server:8000/compare-events"
  text: "{"user_embedding": [0.123, ...], "events": [...]}"
  
When Web2.GotText
  Set similar_events to call JsonTextDecode(responseContent).similar_events
  // Now similar_events is sorted by similarity_score (highest first)
  // Display or process the results
```

### Important for App Inventor Users

When making requests from App Inventor, ensure:
1. The server is accessible from the device/emulator (use actual IP address, not localhost)
2. The JSON payloads are properly formatted as strings
3. Handle responses using JSON decoding

---

## Similarity Score Interpretation

- **1.0**: Perfect similarity (identical text)
- **0.8 - 0.99**: Very similar
- **0.5 - 0.79**: Moderately similar
- **0.2 - 0.49**: Somewhat similar
- **0.0 - 0.19**: Slightly similar
- **Negative values**: Opposite meaning

---

## Embedding Model Details

- **Model**: `all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Language**: Supports 100+ languages
- **Performance**: Fast inference, suitable for mobile apps
- **Training Data**: Trained on sentence-transformers dataset

For more details: https://www.sbert.net/docs/pretrained_models.html

---

## Troubleshooting

### Port Already in Use
```bash
# Run on a different port
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001)"
```

### Model Download Takes Time on First Run
The embedding model is downloaded automatically on first use. This may take a few moments depending on your internet connection.

### CORS Issues
The API has CORS enabled for all origins. If you still encounter issues, check that:
1. The server is running
2. You're using the correct URL and port
3. The request method is POST

---

## Project Structure

```
FASTAPI/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic data models
├── embeddings.py        # Embedding generation logic
├── similarity.py        # Cosine similarity computation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## Performance Notes

- Embedding generation: ~50-100ms per text
- Event comparison: ~1-2ms per event (after embedding)
- Recommended max events per request: 1000+
- Memory usage: ~500MB for the embedding model

---

## License

This project is provided as-is for use with MIT App Inventor and other applications.
