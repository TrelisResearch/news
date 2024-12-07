# The Weekly News (Prediction Market Based News)

Premise = Use polymarket prices to generate news.

Inspiration: Packy McCormack's [Not Boring News](https://www.notboring.co/p/introducing-boring-news)

## Setup
Before running the data collection scripts, you'll need to set up Polymarket API access:

1. **Prerequisites**:
   - A wallet with some MATIC tokens (Polygon network)
   - Your wallet's private key
   - Python dependencies: `pip install py-clob-client python-dotenv`

2. **Environment Setup**:
   - Create a `.env` file in the root directory
   - Add your wallet's private key: `PK=your_private_key_here`
   - Run `python utils/polymarket/create_api_key.py` to generate your API key
   - Add the generated API key to `.env`: `POLYMARKET_API_KEY=your_generated_key`

3. **Verify Setup**:
   - Run `python utils/polymarket/polymarkets.py` to test your connection
   - This will fetch all open markets and save them to `open_markets.txt`

Note: Keep your `.env` file private and never commit it to version control.

## Approach:
A. Data Preparation: Gets "interesting" markets from polymarket.
  1. Fetch markets from polymarket.
  2. Filter the largest 100 markets by volume over the last 7 days.
  3. Prepare price data over last 7 days for the 10 biggest movers out of those 100 top markets.

B. Transcript and voiceover preparation: 
  1. For each interesting market, gets data from perplexity and feeds that to claude to ask for a news transcript.
  2. Feeds the transcript that to ElevenLabs (or a local TTS model) to make a News Podcast (ideally downloadable in vtt format with timestamps).

C. Graphics Generation + Human Presenter (bonus):
  i) For each interesting market, generates plots and or finds relevant images.
  ii) Uses claude to assign timestamps for the content.
  iii) Programatically turn that into a video.
  iv) Create a video presenter that appears to the corner of the video screen, with body language and mouth moving in line with the video.

## Where help is needed?
- Feel free to volunteer for any of A through C. Each should be built in isolation so that it plugs into the rest.
