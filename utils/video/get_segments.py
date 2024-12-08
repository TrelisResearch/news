import os
import sys
from pathlib import Path
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

def get_segments_from_vtt(vtt_path: Path) -> list:
    """Use Claude to identify segments from VTT file and generate image prompts"""
    
    # Load VTT file
    with open(vtt_path) as f:
        vtt_content = f.read()
    
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    system_prompt = """You are helping to create a video news report.
    Analyze the provided VTT transcript and identify 5 segments:
    1. Intro segment (first few seconds)
    2. Three main news segments
    3. Exit/conclusion segment (last few seconds)
    
    For each segment:
    1. Identify the exact start and end timestamps from the VTT
    2. Create a descriptive DALL-E image generation prompt
    
    Return your response as a raw JSON object without any markdown formatting or code blocks.
    
    Format your response as JSON with this structure:
    {
        "segments": [
            {
                "topic": "Brief topic description",
                "start_time": "00:00:00.000",
                "end_time": "00:00:00.000",
                "text": "Full text of the segment",
                "image_prompt": "Detailed prompt for DALL-E image generation"
            }
        ]
    }
    
    Guidelines for image prompts:
    - Start each prompt with "NO TEXT OR WATERMARKS: "
    - Be specific and descriptive
    - Focus on visual elements that represent the topic
    - Request professional, news-style imagery
    - For intro/exit, use professional news studio imagery
    - Specify 'photorealistic' style
    
    Example image prompts:
    - Intro: "NO TEXT OR WATERMARKS: A modern, well-lit news studio desk with professional lighting and broadcast equipment, photorealistic style"
    - News: "NO TEXT OR WATERMARKS: The US Capitol building at dusk with dramatic lighting, showing official government activity, photorealistic style"
    - Exit: "NO TEXT OR WATERMARKS: A professional news studio from a wide angle showing multiple camera setups and technical equipment, photorealistic style"
    """
    
    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the VTT transcript, please identify all 5 segments with their exact timestamps:\n\n{vtt_content}"
                }
            ]
        )
        
        # Clean up Claude's response - remove markdown if present
        response_text = message.content[0].text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        
        # Parse Claude's response
        segments = json.loads(response_text.strip())
        
        # Validate we have exactly 5 segments
        if len(segments["segments"]) != 5:
            print(f"Error: Found {len(segments['segments'])} segments, expected 5")
            return None
            
        return segments["segments"]
        
    except Exception as e:
        print(f"Error getting segments from Claude: {e}")
        print(f"Claude's response: {message.content[0].text if 'message' in locals() else 'No response'}")
        return None