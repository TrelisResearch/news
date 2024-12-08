import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

import cv2
import numpy as np
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image
from utils.image_generation.generate_image import generate_image
from utils.video.get_segments import get_segments_from_vtt
import ffmpeg

def get_latest_files():
    """Get the most recent audio and VTT files"""
    audio_dir = Path("generated_audio")
    audio_files = list(audio_dir.glob("market_news_*.mp3"))
    latest_audio = max(audio_files, key=os.path.getctime)
    
    transcript_dir = Path("market_data/transcripts")
    vtt_files = list(transcript_dir.glob("transcript_*.vtt"))
    latest_vtt = max(vtt_files, key=os.path.getctime)
    
    return latest_audio, latest_vtt

def download_and_resize_image(url: str) -> np.ndarray:
    """Download image and resize to YouTube dimensions (1920x1080)"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate dimensions to maintain aspect ratio
        target_ratio = 16/9
        current_ratio = img.width / img.height
        
        if current_ratio > target_ratio:
            # Image is too wide
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is too tall
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        # Resize to 1920x1080
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
        # Convert to OpenCV format (BGR)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def parse_timestamp(timestamp: float) -> float:
    """Convert timestamp to seconds - handles both string and float formats"""
    if isinstance(timestamp, str):
        # Handle HH:MM:SS.mmm format
        parts = timestamp.split(':')
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        # Already in seconds
        return float(timestamp)

def create_video(audio_path: Path, vtt_path: Path) -> str:
    """Create a video from audio and VTT transcript"""
    # Get segments and image prompts from Claude
    segments = get_segments_from_vtt(vtt_path)
    if not segments:
        print("Failed to get segments from transcript")
        return None
    
    # Video writer setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("generated_video")
    output_dir.mkdir(exist_ok=True)
    
    temp_video_path = output_dir / f"temp_{timestamp}.mp4"
    final_path = output_dir / f"market_news_{timestamp}.mp4"
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 24
    out = cv2.VideoWriter(str(temp_video_path), fourcc, fps, (1920, 1080))
    
    # Calculate total duration from audio file
    audio_info = ffmpeg.probe(str(audio_path))
    total_duration = float(audio_info['streams'][0]['duration'])
    
    # Generate video for each segment
    current_time = 0.0
    for segment in segments:
        start = parse_timestamp(segment["start_time"])
        end = parse_timestamp(segment["end_time"])
        duration = end - start
        n_frames = int(duration * fps)
        
        print(f"\nGenerating image for topic: {segment['topic']}")
        print(f"Using prompt: {segment['image_prompt']}")
        print(f"Duration: {duration:.2f} seconds ({n_frames} frames)")
        
        # Generate image using DALL-E
        image_url = generate_image(segment["image_prompt"], size="1792x1024")
        
        if image_url:
            print("Downloading and processing image...")
            frame = download_and_resize_image(image_url)
            
            if frame is not None:
                print(f"Writing {n_frames} frames...")
                # Write frame multiple times for duration
                for _ in range(n_frames):
                    out.write(frame)
                current_time += duration
    
    # If there's any remaining time, extend the last frame
    if current_time < total_duration:
        remaining_frames = int((total_duration - current_time) * fps)
        print(f"\nAdding {remaining_frames} frames to match audio duration...")
        for _ in range(remaining_frames):
            out.write(frame)
    
    out.release()
    print("\nVideo frames written, adding audio...")
    
    # Combine with audio using ffmpeg
    ffmpeg_cmd = (
        f'ffmpeg -i "{temp_video_path}" -i "{audio_path}" '
        f'-c:v libx264 -preset medium -crf 23 '
        f'-c:a aac -b:a 128k -shortest "{final_path}"'
    )
    result = os.system(ffmpeg_cmd)

    if result != 0:
        print(f"Error running ffmpeg command: {ffmpeg_cmd}")
        return None
    
    os.remove(temp_video_path)
    
    return str(final_path)

if __name__ == "__main__":
    audio_file, vtt_file = get_latest_files()
    video_path = create_video(audio_file, vtt_file)
    print(f"\nVideo generated: {video_path}") 