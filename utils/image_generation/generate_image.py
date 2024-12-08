import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse

def generate_image(prompt, size="1024x1024", model="dall-e-3"):
    """
    Generate an image using DALL-E based on the provided prompt
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        # Generate the image
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality="standard",
            n=1
        )
        
        # Return the URL of the generated image
        return response.data[0].url
    
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate an image using DALL-E')
    parser.add_argument('prompt', type=str, help='The prompt to generate the image from')
    parser.add_argument('--size', type=str, default="1024x1024", 
                      help='Size of the image (1024x1024, 1792x1024, or 1024x1792)')
    parser.add_argument('--model', type=str, default="dall-e-3",
                      help='Model to use (dall-e-2 or dall-e-3)')
    
    args = parser.parse_args()
    
    image_url = generate_image(args.prompt, args.size, args.model)
    if image_url:
        print(f"Generated image URL: {image_url}")

if __name__ == "__main__":
    main() 