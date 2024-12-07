from dotenv import load_dotenv
import os
import requests
from typing import Dict, List
import json

load_dotenv()

def get_open_markets(limit: int = 3) -> List[Dict]:
    """Get top open markets by volume from indexed data.
    
    Args:
        limit: Maximum number of markets to return (default 3)
    
    Returns:
        List of highest-volume markets with their basic info
    """
    host = "https://gamma-api.polymarket.com"
    
    # Get all open markets (no limit)
    params = {
        'active': True,
        'closed': False
    }
    
    response = requests.get(f"{host}/markets", params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching markets: {response.text}")
        
    try:
        markets = response.json()
        
        # Print raw data for first market
        if markets:
            print("\nRaw market data example:")
            print(markets[0])
            
        processed = [
            {
                'question': m['question'],
                'volume': float(m['volumeNum']),
                'volume_24h': float(m.get('volume24hr', 0)),
                'competitive_score': float(m.get('competitive', 0)),
                'last_trade': float(m.get('lastTradePrice', 0)),
                'end_date': m['endDate'],
                'token_id': m['conditionId'],
                'market_id': m.get('id'),
                'clob_token_ids': json.loads(m.get('clobTokenIds', '[]'))
            }
            for m in markets
        ]
        
        # Sort by volume and take top N
        return sorted(processed, key=lambda x: x['volume'], reverse=True)[:limit]
        
    except ValueError:
        raise ValueError("Invalid JSON response from API")

if __name__ == "__main__":
    markets = get_open_markets()
    for m in markets:
        print(f"\nMarket: {m['question']}")
        print(f"Volume: ${m['volume']:,.2f}")
        print(f"24h Volume: ${m['volume_24h']:,.2f}")
        print(f"Competitive Score: {m['competitive_score']:.3f}")
        print(f"Last Trade: ${m['last_trade']:.3f}")