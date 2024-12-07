from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List
from pprint import pprint

load_dotenv()

class PolymarketClient:
    def __init__(self):
        self.host = "https://clob.polymarket.com"
        self.api_key = os.getenv("POLYMARKET_API_KEY")
        self.headers = {"POLY-API-KEY": self.api_key}

    def get_markets(self, next_cursor: str = "") -> Dict:
        """Fetch markets from Polymarket API."""
        url = f"{self.host}/markets"
        if next_cursor:
            url += f"?next_cursor={next_cursor}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching markets: {response.text}")
        return response.json()

    def get_price_history(self, token_id: str, days: int = 7) -> Dict:
        """Get price history for a token over the last N days."""
        end_ts = int(datetime.now(timezone.utc).timestamp())
        start_ts = end_ts - (days * 24 * 60 * 60)
        
        url = f"{self.host}/prices-history"
        params = {
            "market": token_id,
            "startTs": start_ts,
            "endTs": end_ts,
            "fidelity": 60  # 1-hour intervals
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching price history: {response.text}")
        return response.json()

def get_open_markets(limit: int = None) -> List[Dict]:
    """Get open (active, non-closed) markets.
    
    Args:
        limit: Optional maximum number of markets to return
    
    Returns:
        List of markets, each containing basic info and token data
    """
    client = PolymarketClient()
    open_markets = []
    next_cursor = ""
    
    while True:
        response = client.get_markets(next_cursor=next_cursor)
        
        # Filter for active, non-closed markets
        markets = [
            {
                'question': m['question'],
                'token_id': m['tokens'][0]['token_id'] if m['tokens'] else None,
                'volume': float(m.get('volume', 0)),
                'current_price': float(m['tokens'][0]['price']) if m['tokens'] else None
            }
            for m in response['data']
            if m['active'] and not m['closed'] and m['tokens']
        ]
        open_markets.extend(markets)
        
        # Check if we've hit our limit
        if limit and len(open_markets) >= limit:
            open_markets = open_markets[:limit]
            break
            
        next_cursor = response.get('next_cursor', "")
        if not next_cursor or next_cursor == 'LTE=':
            break
    
    return open_markets

def get_market_volume(market_data: Dict) -> float:
    """Get trading volume for a market.
    
    Args:
        market_data: Market data dictionary from get_open_markets()
    
    Returns:
        Volume in USDC
    """
    # Volume is already included in market data from the API
    return market_data['volume']

def get_price_history(token_id: str, days: int = 7) -> List[Dict]:
    """Get hourly price history for a token over last N days.
    
    Args:
        token_id: The token ID to get history for
        days: Number of days of history to get
        
    Returns:
        List of price points, each containing timestamp and price
    """
    client = PolymarketClient()
    history = client.get_price_history(token_id, days)
    return history.get('history', [])

if __name__ == "__main__":
    # Example usage
    print("Getting open markets...")
    markets = get_open_markets(limit=5)  # Get first 5 open markets
    
    for market in markets:
        print(f"\nMarket: {market['question']}")
        print(f"Volume: ${market['volume']:,.2f}")
        print(f"Current Price: {market['current_price']:.3f}")
        
        if market['token_id']:
            print("Getting price history...")
            history = get_price_history(market['token_id'])
            if history:
                prices = [float(point['p']) for point in history]
                print(f"Price range over 7 days: {min(prices):.3f} - {max(prices):.3f}") 