from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timezone
from typing import Dict, List

load_dotenv()

def get_price_history(token_id: str, days: int = 7) -> List[Dict]:
    """Get hourly price history for a token over last N days."""
    host = "https://clob.polymarket.com"
    
    end_ts = int(datetime.now(timezone.utc).timestamp())
    start_ts = end_ts - (days * 24 * 60 * 60)
    
    url = f"{host}/prices-history"
    params = {
        "market": token_id,
        "startTs": start_ts,
        "endTs": end_ts,
        "fidelity": 60  # 1-hour intervals
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching price history: {response.text}")
        
    data = response.json()
    history = data.get('history', [])
    
    if not history:
        print(f"No history found for token {token_id}")
        
    return history

if __name__ == "__main__":
    # Example token ID - you'll need to provide a real one
    token_id = "0x9fce1292bea6748addd9a96632ab7455f64028671816e964a692686573079574"
    history = get_price_history(token_id)
    
    if history:
        prices = [float(point['p']) for point in history]
        print(f"Price range over 7 days: {min(prices):.3f} - {max(prices):.3f}")
        print(f"Number of price points: {len(prices)}") 