import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Update imports with correct paths
from utils.polymarket.find_volatile_markets import find_volatile_markets
from utils.format_market_report import format_market_report, load_market_data, get_latest_market_file
from utils.claude.generate_transcript import generate_news_transcript
from utils.elevenlabs.generate_audio import generate_audio, play_audio
from datetime import datetime
import os

def generate_market_news(market_limit: int = 50, days: int = 7, top_volatile: int = 3, play_audio_file: bool = True):
    """
    Generate a complete news broadcast script from Polymarket data and convert it to audio
    
    Args:
        market_limit: Number of top markets to analyze
        days: Number of days of price history to analyze
        top_volatile: Number of most volatile markets to include
        play_audio_file: Whether to play the generated audio file
    """
    try:
        # 1. Find volatile markets and save data
        print("Finding volatile markets...")
        volatile_markets = find_volatile_markets(
            market_limit=market_limit,
            days=days,
            top_volatile=top_volatile
        )
        
        # 2. Load the saved market data
        latest_file = get_latest_market_file()
        market_data = load_market_data(latest_file)
        
        # 3. Format the market report
        print("\nFormatting market report...")
        market_report = format_market_report(market_data)
        
        # 4. Generate the news transcript
        print("\nGenerating news transcript...")
        transcript = generate_news_transcript(market_report)
        
        if transcript:
            # Save the transcript
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = "market_data"
            os.makedirs(output_dir, exist_ok=True)
            transcript_file = f"{output_dir}/market_news_{timestamp}.txt"
            
            with open(transcript_file, 'w') as f:
                f.write(transcript)
            
            print(f"\nNews transcript saved to: {transcript_file}")
            print("\nTranscript Preview:")
            print("="*80)
            print(transcript[:500] + "...\n")
            
            # Generate audio from the transcript
            print("\nGenerating audio...")
            audio_path = generate_audio(
                text=transcript,
                output_filename=f"market_news_{timestamp}.mp3"
            )
            
            # Play the audio if requested
            if play_audio_file:
                print("\nPlaying audio...")
                play_audio(audio_path)
            
            return transcript, audio_path
        else:
            print("Failed to generate transcript")
            return None, None
            
    except Exception as e:
        print(f"Error generating market news: {str(e)}")
        return None, None

if __name__ == "__main__":
    generate_market_news() 