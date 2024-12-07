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

def calculate_max_return(prices: List[float]) -> float:
    """Calculate maximum possible return given a price series.
    
    Finds the maximum return possible by buying at the lowest price
    and selling at the highest subsequent price.
    """
    if not prices:
        return 0.0
        
    max_return = 0.0
    min_price_so_far = float('inf')
    
    for price in prices:
        if price < min_price_so_far:
            min_price_so_far = price
        else:
            current_return = (price - min_price_so_far) / min_price_so_far
            max_return = max(max_return, current_return)
            
    return max_return

def save_volatile_markets_data(volatile_markets: List[Dict], histories: Dict[str, List]) -> None:
    """Save detailed data about volatile markets to a JSON file, including news from Perplexity.
    
    Args:
        volatile_markets: List of volatile market data
        histories: Dictionary mapping token IDs to their price histories
    """
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
            'max_return': market['max_return'],
            'price_range': {
                'min': market['min_price'],
                'max': market['max_price']
            },
            'news': news_data if news_data else {},  # Add news data
            'token_data': {
                'yes': {
                    'token_id': market['token_ids'][0],
                    'price_history': [
                        {
                            'timestamp': point['t'],
                            'price': float(point['p'])
                        }
                        for point in histories.get(market['token_ids'][0], [])
                    ]
                },
                'no': {
                    'token_id': market['token_ids'][1],
                    'price_history': [
                        {
                            'timestamp': point['t'],
                            'price': float(point['p'])
                        }
                        for point in histories.get(market['token_ids'][1], [])
                    ]
                }
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
                         top_volatile: int =5) -> List[Dict]:
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
    print("\nMarket volumes for verification:")
    for i, m in enumerate(markets[:5], 1):
        print(f"{i}. ${m['volume']:,.2f} - {m['question'][:50]}...")

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
            print(f"CLOB Token IDs: {market['clob_token_ids']}")
            
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
                    all_histories[token_id] = history  # Store history for later
                else:
                    print("No history found for this token")
            
            if histories:
                markets_with_history += 1
                # Calculate max return across both tokens
                max_returns = []
                token_ranges = []
                for j, history in enumerate(histories):
                    prices = [float(point['p']) for point in history]
                    max_return = calculate_max_return(prices)
                    print(f"{'YES' if j==0 else 'NO'} token max return: {max_return*100:.1f}%")
                    print(f"{'YES' if j==0 else 'NO'} price range: ${min(prices):.3f} - ${max(prices):.3f}")
                    max_returns.append(max_return)
                    token_ranges.append((min(prices), max(prices)))
                
                # Use the maximum return from either token
                market_max_return = max(max_returns)
                max_return_idx = max_returns.index(market_max_return)
                print(f"Market max return: {market_max_return*100:.1f}%")
                
                market_data = {
                    'question': market['question'],
                    'volume': market['volume'],
                    'volume_24h': market['volume_24h'],
                    'max_return': market_max_return,
                    'price_points': len(histories[0]),
                    'current_price': prices[-1] if prices else None,
                    'token_ids': market['clob_token_ids'],
                    'min_price': token_ranges[max_return_idx][0],
                    'max_price': token_ranges[max_return_idx][1],
                    'is_yes_token': max_return_idx == 0
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
    
    print(f"\nFound {len(volatile_markets)} markets with price history")
    
    # Sort by max return and get top N
    top_markets = sorted(volatile_markets, 
                        key=lambda x: x['max_return'], 
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