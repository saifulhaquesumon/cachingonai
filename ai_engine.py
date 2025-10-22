import time

def get_ai_response(query: str) -> str:
    """
    A mock function to simulate a call to an AI service.
    """
    print("AI Engine: Generating response...")
    # Simulate a delay for the AI response generation
    time.sleep(2)
    return f"AI response to: {query}"
