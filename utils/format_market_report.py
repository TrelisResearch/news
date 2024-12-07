import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

def load_market_data(filename: str) -> Dict:
    """Load market data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def format_price_history(price_history: List[Dict]) -> str:
    """Format price history into a readable summary."""
    if not price_history:
        return "No price history available"
    
    # Convert timestamps to dates and sort
    dated_prices = [(datetime.fromtimestamp(p['timestamp']).strftime('%Y-%m-%d'), p['price']) 
                   for p in price_history]
    dated_prices.sort(key=lambda x: x[0])
    
    # Get first, last, highest, and lowest prices
    first_price = dated_prices[0]
    last_price = dated_prices[-1]
    highest_price = max(dated_prices, key=lambda x: x[1])
    lowest_price = min(dated_prices, key=lambda x: x[1])
    
    return (f"Price movement from ${first_price[1]:.3f} on {first_price[0]} "
            f"to ${last_price[1]:.3f} on {last_price[0]}.\n"
            f"Highest: ${highest_price[1]:.3f} on {highest_price[0]}\n"
            f"Lowest: ${lowest_price[1]:.3f} on {lowest_price[0]}")

def format_market_report(market_data: Dict) -> str:
    """Format a single market's data into a structured report."""
    market = market_data['markets'][0]  # Assuming we're looking at the most volatile market
    
    report = f"""
MARKET ANALYSIS REPORT
Generated: {market_data['timestamp']}

MARKET QUESTION:
{market['question']}

MARKET METRICS:
- Total Trading Volume: ${market['volume']:,.2f}
- 24h Trading Volume: ${market['volume_24h']:,.2f}
- Maximum Return Opportunity: {market['max_return']*100:.1f}%
- Price Range: ${market['price_range']['min']:.3f} to ${market['price_range']['max']:.3f}

PRICE HISTORY:
YES Token ({market['token_data']['yes']['token_id']}):
{format_price_history(market['token_data']['yes']['price_history'])}

NO Token ({market['token_data']['no']['token_id']}):
{format_price_history(market['token_data']['no']['price_history'])}

RECENT NEWS:
{market['news'].get('content', 'No news available')}

NEWS SOURCES:
"""
    
    if market['news'].get('citations'):
        for citation in market['news']['citations']:
            report += f"- {citation}\n"
    else:
        report += "No citations available\n"
    
    return report

def get_latest_market_file() -> str:
    """Get the most recent volatile markets JSON file."""
    market_data_dir = Path("market_data")
    json_files = list(market_data_dir.glob("volatile_markets_*.json"))
    if not json_files:
        raise FileNotFoundError("No market data files found")
    
    # Sort by modification time and get the most recent
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    return str(latest_file)

if __name__ == "__main__":
    try:
        # Get the latest file by default
        latest_file = get_latest_market_file()
        print(f"Loading data from: {latest_file}")
        
        # Load and format the data
        market_data = load_market_data(latest_file)
        report = format_market_report(market_data)
        
        # Save the formatted report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"market_data/market_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\nReport saved to: {report_file}")
        print("\nReport Preview:")
        print("="*80)
        print(report[:500] + "...\n")
        
    except Exception as e:
        print(f"Error generating report: {str(e)}") 