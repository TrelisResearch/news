import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_latest_suggestions():
    """Get the most recent image suggestions file"""
    suggestions_dir = Path("market_data/video")
    suggestion_files = list(suggestions_dir.glob("image_suggestions_*.json"))
    return max(suggestion_files, key=os.path.getctime)

def search_images(suggestions: dict) -> dict:
    """
    Search for images using Bing Image Search API with rate limiting
    """
    subscription_key = os.getenv("BING_SEARCH_KEY")
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    
    results = {"segments": []}
    
    for segment in suggestions["segments"]:
        segment_results = {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            "images": []
        }
        
        # Search for each suggested term
        for search_term in segment["image_searches"]:
            try:
                params = {
                    "q": search_term,
                    "license": "public",
                    "imageType": "photo",
                    "count": 3
                }
                
                # Add delay between requests
                time.sleep(0.4)  # ~2.5 requests per second to stay under limit
                
                print(f"Searching for: {search_term}")
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                
                search_results = response.json()
                
                # Add top 3 image URLs for this search term
                segment_results["images"].extend([
                    {
                        "url": img["contentUrl"],
                        "search_term": search_term,
                        "thumbnail": img.get("thumbnailUrl", "")  # Also save thumbnail URL
                    }
                    for img in search_results["value"][:3]
                ])
                
                print(f"Found {len(search_results['value'][:3])} images")
                
            except Exception as e:
                print(f"Error searching for '{search_term}': {e}")
                # If we hit rate limit, wait longer before next request
                if "429" in str(e):
                    print("Rate limit hit, waiting 5 seconds...")
                    time.sleep(5)
                continue
        
        results["segments"].append(segment_results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("market_data/video")
    output_path = output_dir / f"image_results_{timestamp}.json"
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    return results

if __name__ == "__main__":
    suggestions_file = get_latest_suggestions()
    with open(suggestions_file) as f:
        suggestions = json.load(f)
    results = search_images(suggestions)
    print("Image search complete!") 