# Prediction Market Based News

Premise = Use polymarket prices to generate news.

Inspiration: Packy McCormack's [Not Boring News](https://www.notboring.co/p/introducing-boring-news)

## Minimal Build - Weekly News
Functionality:
A. Data Preparation: Gets "interesting" markets from polymarket.
  1. Fetch markets from polymarket.
  2. Sort markets according to size. (Filter out all markets below a threshold size).
  3. Sort markets according to number of comments, over the last 7 days.
  4. Sort markets by price movement over last seven days. (possibly should use log(price)).
  5. Prepare data [price trends, number of comments, volume] for the top 5 largest markets and top 5 largest moves.
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
