from dotenv import load_dotenv
import os
import requests
from typing import Dict, List
import json

load_dotenv()

def get_open_markets(limit: int = 100) -> List[Dict]:
    """Get top open markets by volume from indexed data."""
    host = "https://gamma-api.polymarket.com"
    all_markets = []
    offset = 0
    page_size = 20  # API seems to return 20 markets per page
    page = 1
    
    while True:
        print(f"\nFetching page {page}...")
        
        params = {
            'active': True,
            'closed': False,
            'limit': page_size,
            'offset': offset
        }
        
        response = requests.get(f"{host}/markets", params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching markets: {response.text}")
            
        try:
            markets = response.json()
            print(f"Retrieved {len(markets)} markets on this page")
            
            if not markets:  # No more markets to fetch
                break
                
            # Print raw data for first market on first page
            if page == 1 and markets:
                print("\nRaw market data example:")
                print(json.dumps(markets[0], indent=2))
                
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
                if m.get('volumeNum') is not None  # Filter out markets without volume
            ]
            
            print(f"Processed {len(processed)} valid markets from this page")
            all_markets.extend(processed)
            
            if len(all_markets) >= limit:
                print(f"Reached desired limit of {limit} markets")
                break
                
            offset += page_size
            page += 1
            
        except ValueError as e:
            raise ValueError(f"Invalid JSON response from API: {str(e)}")
    
    # Sort by volume and take top N
    sorted_markets = sorted(all_markets, key=lambda x: x['volume'], reverse=True)[:limit]
    print(f"\nReturning top {len(sorted_markets)} markets by volume")
    
    return sorted_markets

if __name__ == "__main__":
    markets = get_open_markets()
    for m in markets:
        print(f"\nMarket: {m['question']}")
        print(f"Volume: ${m['volume']:,.2f}")
        print(f"24h Volume: ${m['volume_24h']:,.2f}")
        print(f"Competitive Score: {m['competitive_score']:.3f}")
        print(f"Last Trade: ${m['last_trade']:.3f}")