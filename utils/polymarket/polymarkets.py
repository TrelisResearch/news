from dotenv import load_dotenv
import os
import requests
import json
from typing import Dict
from pprint import pprint

load_dotenv()

class PolymarketClient:
    def __init__(self):
        self.host = "https://clob.polymarket.com"
        self.api_key = os.getenv("POLYMARKET_API_KEY")
        self.headers = {
            "POLY-API-KEY": self.api_key
        }

    def get_markets(self, next_cursor: str = "") -> Dict:
        """Fetch markets from Polymarket API."""
        url = f"{self.host}/markets"
        if next_cursor:
            url += f"?next_cursor={next_cursor}"
        
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching markets: {response.text}")
        return response.json()

def inspect_market_data():
    """Get a single page of market data and inspect its structure."""
    client = PolymarketClient()
    
    # Get first page of markets
    response = client.get_markets()
    
    # Basic info about the response
    print("\nResponse Keys:", response.keys())
    
    # Look at pagination info
    print("\nPagination Info:")
    print(f"Count: {response.get('count')}")
    print(f"Limit: {response.get('limit')}")
    print(f"Next Cursor: {response.get('next_cursor')}")
    
    # Look at first market in detail
    if response.get('data') and len(response['data']) > 0:
        print("\nFirst Market Structure:")
        first_market = response['data'][0]
        print("\nKeys in market object:", first_market.keys())
        
        print("\nDetailed first market data:")
        pprint(first_market)
        
        # Save raw response for further inspection
        with open('sample_market_response.json', 'w') as f:
            json.dump(response, f, indent=2)
        print("\nFull response saved to sample_market_response.json")
    else:
        print("No markets found in response")

if __name__ == "__main__":
    inspect_market_data()
