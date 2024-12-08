import os
from pathlib import Path
import whisper
import json
from datetime import datetime

def get_latest_audio_file():
    """Get the most recently generated audio file"""
    audio_dir = Path("generated_audio")
    audio_files = list(audio_dir.glob("market_news_*.mp3"))
    return max(audio_files, key=os.path.getctime)

def generate_transcript(audio_path: Path) -> dict:
    """
    Transcribe audio file using Whisper and return segments with timestamps
    """
    # Load the smallest model for speed
    model = whisper.load_model("tiny")
    
    # Transcribe with word-level timestamps
    result = model.transcribe(
        str(audio_path),
        word_timestamps=True,
        verbose=False
    )
    
    # Save both the VTT and structured data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("market_data/transcripts")
    output_dir.mkdir(exist_ok=True)
    
    # Save VTT file
    with open(output_dir / f"transcript_{timestamp}.vtt", "w") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")
    
    # Save structured JSON
    with open(output_dir / f"transcript_{timestamp}.json", "w") as f:
        json.dump(result, f, indent=2)
    
    return result

def format_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

if __name__ == "__main__":
    latest_audio = get_latest_audio_file()
    transcript = generate_transcript(latest_audio)
    print("Transcription complete!") 