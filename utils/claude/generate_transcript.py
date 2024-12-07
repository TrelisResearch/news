import os
import anthropic
from dotenv import load_dotenv
from datetime import datetime

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
         * The exact probability change over the week (e.g., "from 35% to 42%")
         * Brief context for why this movement occurred
    3. Quick wrap-up (10 seconds)
    
    Guidelines:
    - Be concise and direct
    - Always mention specific probability changes
    - Never mention YES/NO tokens - only discuss probabilities of events occurring
    - Use clear, professional language
    - Keep the tone measured and factual
    - Focus on concrete probability changes and their implications
    
    Important:
    - Start directly with the news content
    - Do not include any meta text or prefixes
    - Do not include any speaker attributions or dialogue markers
    - Keep the entire script to approximately 150-175 words"""
    
    try:
        # Save the prompt and market report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_dir = "market_data/prompts"
        os.makedirs(prompt_dir, exist_ok=True)
        
        with open(f"{prompt_dir}/claude_prompt_{timestamp}.txt", 'w') as f:
            f.write("SYSTEM PROMPT:\n")
            f.write("=============\n")
            f.write(system_prompt)
            f.write("\n\nMARKET REPORT:\n")
            f.write("=============\n")
            f.write(market_report)
        
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
        
        # Save Claude's response
        with open(f"{prompt_dir}/claude_response_{timestamp}.txt", 'w') as f:
            f.write(message.content[0].text)
        
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