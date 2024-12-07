import os
import requests
from typing import Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def query_perplexity(topic: str, time_window: str = "day") -> Dict[Any, Any]:
    """
    Query the Perplexity API for news on a specific topic.
    
    Args:
        topic (str): The topic to search for news about
        time_window (str): Time window for search results ('month', 'week', 'day', 'hour')
    
    Returns:
        Dict: The API response
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY not found in .env file")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides concise news summaries."
            },
            {
                "role": "user",
                "content": f"What are the latest developments regarding {topic}? Please provide a brief summary with sources."
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "include_citations": True,
        "stream": False
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract the relevant information
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = result.get("citations", [])
        
        return {
            "content": content,
            "citations": citations
        }
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    topic = "artificial intelligence"
    result = query_perplexity(topic)
    
    if result:
        print("\nSummary:")
        print(result["content"])
        
        if result["citations"]:
            print("\nSources:")
            for citation in result["citations"]:
                print(f"- {citation}") 