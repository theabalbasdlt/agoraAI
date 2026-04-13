# Quick Start Guide

## Installation & Setup (Windows)

### Step 1: Install Python
Ensure you have Python 3.8+ installed on your system.

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- Numpy: Numerical operations
- scikit-learn: Similarity calculations
- sentence-transformers: Embedding model
- python-multipart: Form data handling

**Note**: On first run, the embedding model (~100MB) will be downloaded automatically. This may take 1-2 minutes.

### Step 4: Start the Server
```bash
python main.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 5: Verify the Server
Open your browser and visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Testing the API

### Option A: Using the Interactive Documentation
1. Go to `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Enter the request data
5. Click "Execute"

### Option B: Using the Examples Script
In a separate terminal:
```bash
python examples.py
```

This will demonstrate embedding creation and event comparison without HTTP requests.

### Option C: Using cURL
```bash
# Create an embedding
curl -X POST "http://localhost:8000/create-embedding" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"I enjoy hiking and outdoor activities\"}"

# Compare events (requires previous embeddings)
curl -X POST "http://localhost:8000/compare-events" \
  -H "Content-Type: application/json" \
  -d "{\"user_embedding\": [...], \"events\": [...]}"
```

---

## Integration with MIT App Inventor

### Setup
1. Start the FastAPI server on your computer
2. Find your computer's IP address:
   - **Windows**: Open Command Prompt and type `ipconfig` (look for IPv4 Address)
   - Example: `192.168.1.100`

3. In App Inventor, use Web component with URL: `http://YOUR_IP:8000/create-embedding`

### Example Flow in App Inventor

**When Screen1 Initialize:**
```
Set up user profile text
```

**Create Embedding Button Click:**
```
Call Web1.PostText
  url: "http://192.168.1.100:8000/create-embedding"
  text: "{\"text\": \"" + userProfileText + "\"}"

When Web1.GotText
  Set userEmbedding to JsonTextDecode(responseContent).embedding
  Set embeddingCreated to true
  Show notification "Embedding created"
```

**Compare Events Button Click:**
```
Call Web2.PostText
  url: "http://192.168.1.100:8000/compare-events"
  text: BuildComparisonPayload(userEmbedding, eventsList)

When Web2.GotText
  Set similarEvents to JsonTextDecode(responseContent).similar_events
  Display results sorted by similarity_score
```

---

## Troubleshooting

### Issue: "Address already in use"
The default port 8000 is already in use. Change the port:
```bash
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001)"
```

### Issue: Model Download Issues
If the embedding model download fails:
```bash
# Pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Issue: App Inventor Can't Connect
1. Ensure the server is running
2. Use your computer's actual IP address (not localhost)
3. Firewall: Allow Python through Windows Firewall
4. Mobile/Emulator: Must be on the same network

### Issue: Slow Response
First embedding request downloads the model (~100MB). Subsequent requests are much faster (~50-100ms per embedding).

### Issue: Out of Memory
If running on low-memory systems, use a lighter model in `config.py`:
```python
EMBEDDING_MODEL = "sentence-transformers/all-mini-lm-l12-v1"
```

---

## Project Structure

```
FASTAPI/
├── main.py              # FastAPI application (start here)
├── models.py            # Request/response data models
├── embeddings.py        # Text embedding functions
├── similarity.py        # Cosine similarity computation
├── config.py            # Configuration settings
├── examples.py          # Example usage and testing
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
├── QUICKSTART.md        # This file
└── .gitignore          # Git ignore rules
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Start the server
3. ✅ Test with interactive docs
4. ✅ Integrate with App Inventor
5. Deploy to production (optional)

---

## Production Deployment

For public deployment, consider:
- Using a production ASGI server (Gunicorn + Uvicorn)
- Running behind a reverse proxy (Nginx)
- Adding authentication/API keys
- Using HTTPS/SSL
- Monitoring and logging

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---

For more details, see [README.md](README.md)
