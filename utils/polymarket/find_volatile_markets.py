from typing import Dict, List
from get_markets import get_open_markets
from get_price_history import get_price_history

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

def find_volatile_markets(market_limit: int = 10, 
                         days: int = 7, 
                         top_volatile: int = 3) -> List[Dict]:
    """Find most volatile markets by analyzing price history."""
    # Get top markets by volume
    print(f"Fetching top {market_limit} markets...")
    markets = get_open_markets(limit=market_limit)
    print(f"Found {len(markets)} markets")
    
    # Analyze price history for each market
    volatile_markets = []
    for i, market in enumerate(markets):
        try:
            print(f"\nProcessing market {i+1}/{len(markets)}: {market['question'][:50]}...")
            print(f"CLOB Token IDs: {market['clob_token_ids']}")
            
            # Get price history for both YES and NO tokens
            histories = []
            for j, token_id in enumerate(market['clob_token_ids']):
                print(f"Getting history for {'YES' if j==0 else 'NO'} token {token_id}")
                history = get_price_history(token_id, days=days)
                if history:
                    print(f"Found {len(history)} price points")
                    histories.append(history)
                else:
                    print("No history found")
            
            if histories:
                # Calculate max return across both tokens
                max_returns = []
                for j, history in enumerate(histories):
                    prices = [float(point['p']) for point in history]
                    max_return = calculate_max_return(prices)
                    print(f"{'YES' if j==0 else 'NO'} token max return: {max_return*100:.1f}%")
                    max_returns.append(max_return)
                
                # Use the maximum return from either token
                market_max_return = max(max_returns)
                print(f"Market max return: {market_max_return*100:.1f}%")
                
                market_data = {
                    'question': market['question'],
                    'volume': market['volume'],
                    'volume_24h': market['volume_24h'],
                    'max_return': market_max_return,
                    'price_points': len(histories[0]),
                    'current_price': prices[-1] if prices else None,
                    'token_ids': market['clob_token_ids']
                }
                volatile_markets.append(market_data)
            else:
                print("No price history found for either token")
                
        except Exception as e:
            print(f"Error processing market {market['question']}: {str(e)}")
            continue

    print(f"\nFound {len(volatile_markets)} markets with price history")
    
    # Sort by max return and return top N
    return sorted(volatile_markets, 
                 key=lambda x: x['max_return'], 
                 reverse=True)[:top_volatile]

if __name__ == "__main__":
    volatile_markets = find_volatile_markets()
    
    print("\nMost Volatile Markets:")
    print("=====================")
    
    for i, market in enumerate(volatile_markets, 1):
        print(f"\n{i}. {market['question']}")
        print(f"Max Return: {market['max_return']*100:.1f}%")
        print(f"Volume: ${market['volume']:,.2f}")
        print(f"24h Volume: ${market['volume_24h']:,.2f}")
        print(f"Current Price: ${market['current_price']:.3f}") 