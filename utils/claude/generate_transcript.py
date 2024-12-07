import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

def generate_news_transcript(market_report: str) -> str:
    """
    Generate a news anchor transcript from market report data using Claude 3.5 Haiku
    
    Args:
        market_report (str): The formatted market report to convert into a news transcript
        
    Returns:
        str: The generated news transcript formatted for single speaker narration
    """
    # Initialize Claude client
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Construct the system prompt
    system_prompt = """You are a professional financial news anchor delivering a concise 1-minute weekly market analysis.
    Convert the provided Polymarket data into a clear, informative broadcast covering the top 3 most significant 
    prediction market movements from the past 7 days.
    
    Structure the script with:
    1. A brief introduction mentioning this is the weekly report (5 seconds)
    2. Three notable markets (45 seconds total):
       - Lead with the most significant market movement
       - Cover two additional noteworthy markets
       - For each market, mention:
         * Current probability of the event occurring
         * How that probability changed over the past week
         * Brief context for the movement
    3. Quick wrap-up (10 seconds)
    
    Guidelines:
    - Be concise and direct
    - Express everything as simple probabilities (e.g., "The probability of X happening increased from 25% to 40% this week")
    - Never mention YES/NO tokens - only discuss probabilities of events occurring
    - Use clear, professional language
    - Avoid terms like "dive", "delve", or "deep dive"
    - Keep the tone measured and factual
    - Avoid vague language like "waiting to unfold" or "remains to be seen"
    - Focus on concrete probability changes and their implications
    
    Important:
    - Start directly with the news content
    - Do not include any meta text or prefixes like "Here's the market analysis..."
    - Do not include any speaker attributions or dialogue markers
    - Keep the entire script to approximately 150-175 words"""
    
    try:
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Please convert this weekly market analysis into a measured news broadcast script: {market_report}"
                }
            ]
        )
        
        # Remove any potential prefix text
        transcript = message.content[0].text
        if ":" in transcript.split("\n")[0]:
            transcript = "\n".join(transcript.split("\n")[1:]).strip()
        
        return transcript
        
    except Exception as e:
        print(f"Error generating transcript: {e}")
        return None

if __name__ == "__main__":
    # Test the function with sample text
    sample_text = """
    Breaking research from Stanford University reveals new potential in renewable energy storage.
    The breakthrough could make solar power more viable for overnight use.
    Lead researcher Dr. Sarah Chen calls this a 'game-changing development'.
    """
    
    transcript = generate_news_transcript(sample_text)
    if transcript:
        print("\nGenerated News Transcript:")
        print("-" * 50)
        print(transcript) 