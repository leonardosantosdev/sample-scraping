from spotify_auth import spotify_auth
from sample_scraping import SampleScraping

user_id = "<your spotify user_id>"
client_id = "<your spotify client_id>"
client_secret = "<your spotify cliente_secret>"
genius_url = "https://genius.com/albums/kanye-west/my-beautiful-dark-twisted-fantasy"  # your genius album url

sp = spotify_auth(user_id, client_id, client_secret)
scraping = SampleScraping(user_id, genius_url, sp)

scraping.create_samples_playlist()
