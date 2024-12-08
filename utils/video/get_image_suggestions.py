import os
import json
import anthropic
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_latest_transcript():
    """Get the most recent transcript JSON file"""
    transcript_dir = Path("market_data/transcripts")
    transcript_files = list(transcript_dir.glob("transcript_*.json"))
    return max(transcript_files, key=os.path.getctime)

def get_image_suggestions(transcript_data: dict) -> dict:
    """
    Get image suggestions from Claude for each segment of the transcript
    """
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    system_prompt = """You are a video production assistant helping to find relevant images for a financial news broadcast.
    For each segment of the transcript, suggest 2-3 specific image search terms that would work well as B-roll footage.
    
    Guidelines:
    - Suggest images that are likely to be found in stock photo libraries
    - Focus on professional, business-appropriate imagery
    - Include both literal and metaphorical suggestions
    - Format response as JSON with segment timestamps and image suggestions
    
    Example format:
    {
        "segments": [
            {
                "start": "00:00:00.000",
                "end": "00:00:05.000",
                "text": "Welcome to the Weekly Market Report",
                "image_searches": [
                    "stock market digital display board",
                    "professional news anchor desk",
                    "financial district skyscrapers"
                ]
            }
        ]
    }"""

    try:
        # Prepare the transcript segments for Claude
        segments = [
            {
                "start": format_timestamp(seg["start"]),
                "end": format_timestamp(seg["end"]),
                "text": seg["text"].strip()
            }
            for seg in transcript_data["segments"]
        ]
        
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Please suggest image search terms for these transcript segments: {json.dumps(segments, indent=2)}"
                }
            ]
        )
        
        # Parse Claude's JSON response
        suggestions = json.loads(message.content[0].text)
        
        # Save suggestions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("market_data/video")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / f"image_suggestions_{timestamp}.json", "w") as f:
            json.dump(suggestions, f, indent=2)
            
        return suggestions
        
    except Exception as e:
        print(f"Error getting image suggestions: {e}")
        return None

def format_timestamp(seconds: float) -> str:
    """Convert seconds to timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

if __name__ == "__main__":
    transcript_file = get_latest_transcript()
    with open(transcript_file) as f:
        transcript_data = json.load(f)
    suggestions = get_image_suggestions(transcript_data)
    print("Image suggestions generated!") 