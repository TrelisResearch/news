import os
import cv2
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image

def get_latest_files():
    """Get the most recent audio, transcript and image results"""
    audio_dir = Path("generated_audio")
    audio_files = list(audio_dir.glob("market_news_*.mp3"))
    latest_audio = max(audio_files, key=os.path.getctime)
    
    video_dir = Path("market_data/video")
    image_files = list(video_dir.glob("image_results_*.json"))
    latest_images = max(image_files, key=os.path.getctime)
    
    return latest_audio, latest_images

def download_and_resize_image(url: str, thumbnail_url: str = None) -> np.ndarray:
    """Download image and resize to YouTube dimensions (1920x1080)"""
    urls_to_try = [url]
    if thumbnail_url:
        urls_to_try.insert(0, thumbnail_url)  # Try thumbnail first
        
    for img_url in urls_to_try:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(img_url, headers=headers, timeout=10)
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
            print(f"Error downloading image from {img_url}: {e}")
            continue
    
    print("Failed to download image from all URLs")
    return None

def parse_timestamp(timestamp: str) -> float:
    """Convert timestamp string (HH:MM:SS.mmm) to seconds"""
    parts = timestamp.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def create_video(audio_path: Path, image_data_path: Path) -> str:
    """Create a video from audio and image data"""
    with open(image_data_path) as f:
        image_data = json.load(f)
    
    # Video writer setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("generated_video")
    output_dir.mkdir(exist_ok=True)
    
    # First create video without audio
    temp_video_path = output_dir / f"temp_{timestamp}.mp4"
    final_path = output_dir / f"market_news_{timestamp}.mp4"
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 24
    out = cv2.VideoWriter(str(temp_video_path), fourcc, fps, (1920, 1080))
    
    for segment in image_data["segments"]:
        start = parse_timestamp(segment["start"])
        end = parse_timestamp(segment["end"])
        duration = end - start
        n_frames = int(duration * fps)
        
        if segment["images"]:
            img_data = segment["images"][0]
            frame = download_and_resize_image(
                img_data["url"], 
                img_data.get("thumbnail", None)
            )
            
            if frame is not None:
                # Write frame multiple times for duration
                for _ in range(n_frames):
                    out.write(frame)
    
    out.release()
    
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
    audio_file, image_data = get_latest_files()
    video_path = create_video(audio_file, image_data)
    print(f"\nVideo generated: {video_path}") 