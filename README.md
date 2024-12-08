# The Weekly News (Prediction Market Based News)

Generates news reports based on Polymarket prediction market data, converting market movements into professional news broadcasts with audio and video.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Keys Setup**:
   Create a `.env` file in the root directory with:
   ```
   PK=your_polygon_wallet_private_key
   POLYMARKET_API_KEY=your_polymarket_api_key
   ANTHROPIC_API_KEY=your_claude_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   PERPLEXITY_API_KEY=your_perplexity_api_key
   BING_SEARCH_KEY=your_bing_api_key
   ```

3. **Generate Polymarket API Key**:
   ```bash
   python utils/polymarket/create_api_key.py
   ```

## Usage

1. **Generate Complete News Report**:
   ```bash
   python utils/generate_market_news.py
   ```
   This will:
   - Find volatile markets on Polymarket
   - Generate a news transcript using Claude
   - Create an audio version using ElevenLabs

2. **Generate Video Version**:
   ```bash
   # First generate the transcript and audio
   python utils/generate_market_news.py
   
   # Generate video components
   python utils/whisper/transcribe_audio.py
   python utils/video/get_image_suggestions.py
   python utils/video/search_images.py
   python utils/video/generate_video.py
   ```

3. **Individual Components**:

   a. Find Volatile Markets:
   ```bash
   python utils/polymarket/find_volatile_markets.py
   ```

   b. Generate Transcript Only:
   ```bash
   python utils/claude/generate_transcript.py
   ```

   c. Generate Audio Only:
   ```bash
   python utils/elevenlabs/generate_audio.py
   ```

## Output Files

The scripts generate several files:
- `market_data/volatile_markets_[timestamp].json`: Raw market data
- `market_data/market_news_[timestamp].txt`: Generated news transcript
- `market_data/transcripts/`: Whisper transcriptions with timestamps
- `market_data/video/`: Image suggestions and search results
- `market_data/prompts/`: Claude prompts and responses
- `generated_audio/`: Audio files from ElevenLabs
- `generated_video/`: Final video outputs

## Video Format
- Resolution: 1920x1080 (YouTube standard)
- FPS: 24
- Format: MP4 with H.264 video and AAC audio
- Features:
  - Synchronized audio narration
  - Relevant images for each segment
  - Subtitles overlay

## Project Structure
