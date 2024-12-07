from typing import Dict, List
from .get_markets import get_open_markets
from .get_price_history import get_price_history
import json
from datetime import datetime
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

# Now we can import from utils
from utils.perplexity.test_perplexity import query_perplexity

def calculate_price_ratio(prices: List[float]) -> float:
    """Calculate ratio between max and min prices in a series."""
    if not prices:
        return 1.0
    
    min_price = min(prices)
    max_price = max(prices)
    
    # Avoid division by zero
    if min_price == 0:
        return 1.0
        
    return max_price / min_price

def get_daily_prices(history: List[Dict]) -> List[Dict]:
    """Extract one price per day from history."""
    daily_prices = {}
    
    # Convert timestamps to dates and get last price for each day
    for point in history:
        date = datetime.fromtimestamp(point['t']).strftime('%Y-%m-%d')
        daily_prices[date] = float(point['p'])
    
    # Sort by date and return list of prices
    return [
        {'date': date, 'price': price}
        for date, price in sorted(daily_prices.items())
    ]

def save_volatile_markets_data(volatile_markets: List[Dict], histories: Dict[str, List]) -> None:
    """Save detailed data about volatile markets to a JSON file, including news from Perplexity."""
    output_dir = "market_data"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/volatile_markets_{timestamp}.json"
    
    detailed_markets = []
    for market in volatile_markets:
        print(f"\nFetching news for market: {market['question'][:100]}...")
        
        # Query Perplexity for news about this market
        news_data = query_perplexity(market['question'])
        
        detailed_market = {
            'question': market['question'],
            'volume': market['volume'],
            'volume_24h': market['volume_24h'],
            'daily_prices': market['daily_prices'],
            'news': news_data if news_data else {},
            'token_data': {
                'yes': {'token_id': market['token_ids'][0]},
                'no': {'token_id': market['token_ids'][1]}
            }
        }
        detailed_markets.append(detailed_market)
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'markets': detailed_markets
        }, f, indent=2)
    
    print(f"\nSaved detailed market data with news to {filename}")

def find_volatile_markets(market_limit: int = 10, 
                         days: int = 7, 
                         top_volatile: int = 5) -> List[Dict]:
    """Find most volatile markets by analyzing price history.
    
    Args:
        market_limit: Number of top markets by volume to analyze (default 100)
        days: Number of days of price history to analyze (default 7)
        top_volatile: Number of most volatile markets to return (default 3)
    """
    # Get top markets by volume
    print(f"Fetching top {market_limit} markets...")
    markets = get_open_markets(limit=market_limit)
    print(f"Found {len(markets)} markets")
    
    # Add counter for markets with price history
    markets_with_history = 0
    markets_without_history = 0
    
    # Store all histories for later use
    all_histories = {}
    
    # Analyze price history for each market
    volatile_markets = []
    for i, market in enumerate(markets):
        try:
            print(f"\nProcessing market {i+1}/{len(markets)}: {market['question'][:50]}...")
            print(f"Volume: ${market['volume']:,.2f}")
            
            if not market['clob_token_ids']:
                print("Skipping - No CLOB token IDs found")
                markets_without_history += 1
                continue

            # Get price history for both YES and NO tokens
            histories = []
            for j, token_id in enumerate(market['clob_token_ids']):
                print(f"Getting history for {'YES' if j==0 else 'NO'} token {token_id}")
                history = get_price_history(token_id, days=days)
                if history:
                    print(f"Found {len(history)} price points")
                    histories.append(history)
                    all_histories[token_id] = history
                else:
                    print("No history found for this token")
            
            if histories:
                markets_with_history += 1
                
                # Get daily prices for YES token
                yes_daily = get_daily_prices(histories[0])
                yes_prices = [p['price'] for p in yes_daily]
                latest_yes_price = yes_prices[-1] if yes_prices else None
                
                # Skip markets that are too certain
                if latest_yes_price is None or latest_yes_price < 0.01 or latest_yes_price > 0.99:
                    print("Skipping - Market probability too extreme")
                    continue
                
                # Calculate volatility ratios for both tokens
                yes_ratio = calculate_price_ratio(yes_prices)
                no_daily = get_daily_prices(histories[1])
                no_ratio = calculate_price_ratio([p['price'] for p in no_daily])
                
                # Use the higher ratio for sorting
                volatility_ratio = max(yes_ratio, no_ratio)
                
                market_data = {
                    'question': market['question'],
                    'volume': market['volume'],
                    'volume_24h': market['volume_24h'],
                    'token_ids': market['clob_token_ids'],
                    'daily_prices': {
                        'yes': yes_daily,
                        'no': no_daily
                    },
                    'internal_volatility_score': volatility_ratio
                }
                volatile_markets.append(market_data)
            else:
                print("No price history found for either token")
                markets_without_history += 1
                
        except Exception as e:
            print(f"Error processing market {market['question']}: {str(e)}")
            markets_without_history += 1
            continue

    print(f"\nProcessing Summary:")
    print(f"Total markets fetched: {len(markets)}")
    print(f"Markets with price history: {markets_with_history}")
    print(f"Markets without price history: {markets_without_history}")
    
    # Sort by volatility score and get top N
    top_markets = sorted(volatile_markets, 
                        key=lambda x: x['internal_volatility_score'], 
                        reverse=True)[:top_volatile]
    
    # Save detailed data about top volatile markets
    save_volatile_markets_data(top_markets, all_histories)
    
    return top_markets

if __name__ == "__main__":
    volatile_markets = find_volatile_markets()
    
    print("\nMost Volatile Markets:")
    print("=====================")
    
    for i, market in enumerate(volatile_markets, 1):
        print(f"\n{i}. {market['question']}")
        print(f"Max Return: {market['max_return']*100:.1f}%")
        print(f"Volume: ${market['volume']:,.2f}")
        print(f"24h Volume: ${market['volume_24h']:,.2f}")
        print(f"7d Price Range: ${market['min_price']:.3f} - ${market['max_price']:.3f}") 