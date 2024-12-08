# The Weekly News (Prediction Market Based News)

Generates news reports based on Polymarket prediction market data, converting market movements into professional news broadcasts with audio.

Check the generated_audio/ directory for the output audio files.

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
   - Play the audio (optional)

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

## Output Files

The scripts generate several files in the `market_data` directory:
- `volatile_markets_[timestamp].json`: Raw market data
- `market_news_[timestamp].txt`: Generated news transcript
- `prompts/`: Claude prompts and responses
- `generated_audio/`: Audio files from ElevenLabs

## Project Structure
