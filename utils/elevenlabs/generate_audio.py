import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import pygame

def generate_audio(text, output_filename="output.mp3"):
    """
    Generate audio from text using ElevenLabs API
    
    Args:
        text: The text to convert to speech
        output_filename: Name of the output audio file
    
    Returns:
        str: Path to the generated audio file
    """
    # Load environment variables
    load_dotenv()
    
    # Set API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in .env file")
    
    # Initialize client
    client = ElevenLabs(api_key=api_key)

    # Generate audio with Irish voice and optimal settings for news reading
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="D38z5RcWu1voky8WS1ja",
        model_id="eleven_multilingual_v2",  # Faster, cheaper model
        voice_settings={
            "stability": 0.71,
            "similarity_boost": 0.5,
            "style": 0.0,
            "use_speaker_boost": True
        }
    )

    # Save the audio file
    output_dir = "generated_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Collect all chunks from the generator and write to file
    audio_data = b"".join(chunk for chunk in audio_stream)
    
    with open(output_path, "wb") as f:
        f.write(audio_data)
    
    print(f"Audio generated and saved to {output_path}")
    return output_path

def play_audio(audio_path):
    """
    Play the generated audio file
    
    Args:
        audio_path: Path to the audio file to play
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.quit()

def generate_test_audio():
    """Test function for audio generation and playback"""
    text = """
    Good evening, and welcome to the evening news. 
    Today's top story: Scientists have discovered a new species of butterfly in Ireland, 
    marking a significant breakthrough in local biodiversity research.
    """
    
    audio_path = generate_audio(text, "test_news.mp3")
    play_audio(audio_path)

if __name__ == "__main__":
    generate_test_audio() 