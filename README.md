 # Sample Scraping

This project combines web scraping from Genius and Spotify API integration to create playlists of music samples from a given album.

### Spotify Authentication
Sample Scraping utilizes the Spotipy module for Spotify API authentication. To connect to the Spotify API, the project uses the client credentials flow, obtaining an access token for making requests to the Spotify API. This authentication process is handled in `spotify_auth.py`.

### WebScraping Proccess
The web scraping process involves extracting sample information from the Genius website. Sample Scraping uses the requests library to make HTTP requests, BeautifulSoup for HTML parsing, and difflib for string similarity comparison. This step is under `sample_scraping.py`, with a class containing all functions needed.

### Usage
Before running the script, make sure you have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/). Use a Python version compatible with the project, e.g., Python 3.7 or higher.


First, clone the repository to your machine:

    $ git clone https://github.com/leonardosantosdev/sample-scraping

Under root directory, install the needed modules:

    $ pip install -r requirements.txt

Inside /scripts, change `main.py` with your Spotify credentials and Genius URL for the album that you want to get the samples.

**PS**: Usually, samples are used in rap albums, since sampling is a hip-hop culture. In my example, i put a URL for *My Beautiful Dark Twisted Fantasy* by Kanye West. Feel free to choose yours.
```python 
from spotify_auth import spotify_auth
from sample_scraping import SampleScraping

user_id = "<your spotify user_id>"
client_id = "<your spotify client_id>"
client_secret = "<your spotify cliente_secret>"
genius_url = "https://genius.com/albums/kanye-west/my-beautiful-dark-twisted-fantasy"  # your genius album url

sp = spotify_auth(user_id, client_id, client_secret)
scraping = SampleScraping(user_id, genius_url, sp)

scraping.create_samples_playlist()

```

Simply run `main.py` and the playlist will be created with the samples in your Spotify account.