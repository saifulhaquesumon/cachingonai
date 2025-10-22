import redis
import os

# --- Redis Connection ---
# Use environment variables for Redis configuration with sensible defaults
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    # The decode_responses=True is important to get strings back from Redis
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Check if the connection is successful
    redis_client.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    # In a real application, you might want to handle this more gracefully.
    # For this example, we'll allow the app to continue, but caching will fail.
    redis_client = None

# --- Cache Functions ---
def get_from_cache(key: str):
    """
    Gets a value from the Redis cache.
    Returns the value if the key exists, otherwise returns None.
    """
    if redis_client:
        return redis_client.get(key)
    return None

def set_in_cache(key: str, value: str, expiration_seconds: int = 600):
    """
    Sets a key-value pair in the Redis cache with an expiration time.
    Expiration is set to 10 minutes (600 seconds) by default.
    """
    if redis_client:
        redis_client.setex(key, expiration_seconds, value)
