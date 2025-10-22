from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .cache import get_from_cache, set_in_cache
from .ai_engine import get_ai_response

# Initialize FastAPI app
app = FastAPI(
    title="AI Chatbot with Redis Caching",
    description="An example of using FastAPI and Redis to cache AI responses.",
    version="1.0.0",
)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    response: str
    cached: bool

# --- API Endpoints ---
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Handles a user's chat query.

    1.  Checks for a cached response in Redis.
    2.  If found (cache hit), returns the cached response.
    3.  If not found (cache miss), generates a new response,
        caches it, and then returns it.
    """
    query = request.query
    cache_key = f"query:{query.lower().strip()}"

    # 1. Check cache first
    cached_response = get_from_cache(cache_key)
    if cached_response:
        print(f"Cache HIT for query: '{query}'")
        return ChatResponse(
            query=query,
            response=cached_response,
            cached=True
        )

    # 2. If cache miss, generate response
    print(f"Cache MISS for query: '{query}'")
    ai_response = get_ai_response(query)

    # 3. Store the new response in the cache
    set_in_cache(cache_key, ai_response)

    return ChatResponse(
        query=query,
        response=ai_response,
        cached=False
    )

@app.get("/", summary="Health Check")
def read_root():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "API is running"}
