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
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Install System Dependencies**:
   ```bash
   # On Mac
   brew install ffmpeg
   ```

## Usage

1. **Generate Complete News Report**:
   ```bash
   # Generate transcript and audio
   python utils/generate_market_news.py
   
   # Create video with images
   python utils/whisper/transcribe_audio.py  # Create timestamped transcript
   python utils/video/generate_video.py      # Generate final video
   ```

   This process:
   1. Finds volatile markets on Polymarket
   2. Generates a news transcript using Claude
   3. Creates an audio version using ElevenLabs
   4. Transcribes audio to get precise timestamps
   5. Generates images using DALL-E
   6. Combines everything into a final video

2. **Individual Components**:

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

   d. Generate Video Only (requires existing audio):
   ```bash
   python utils/video/generate_video.py
   ```

## Output Files

The scripts generate several files:
- `market_data/volatile_markets_[timestamp].json`: Raw market data
- `market_data/market_news_[timestamp].txt`: Generated news transcript
- `market_data/transcripts/`: Whisper transcriptions with timestamps
- `market_data/prompts/`: Claude prompts and responses
- `generated_audio/`: Audio files from ElevenLabs
- `generated_video/`: Final video outputs

## Video Format
- Resolution: 1920x1080 (YouTube standard)
- FPS: 24
- Format: MP4 with H.264 video and AAC audio
- Structure:
  - Intro segment with news studio imagery
  - Three main news segments with topic-specific imagery
  - Exit segment with studio imagery
- Features:
  - Professional news-style visuals
  - Synchronized audio narration
  - Photorealistic DALL-E generated images
  - Seamless transitions between segments

## Project Structure
```
.
├── generated_audio/     # ElevenLabs audio outputs
├── generated_video/     # Final video outputs
├── market_data/        # Data and intermediate files
│   ├── prompts/       # Claude interactions
│   ├── transcripts/   # Whisper transcriptions
│   └── video/        # Video generation data
└── utils/             # Core functionality
    ├── claude/       # Transcript generation
    ├── elevenlabs/   # Audio generation
    ├── polymarket/   # Market data collection
    ├── video/        # Video assembly
    └── whisper/      # Audio transcription
```
