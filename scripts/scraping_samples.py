import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
from difflib import SequenceMatcher as sm

USER_ID = "12164987210"
CLIENT_ID = "230afda5856c4e5899ad77dd49bc1e3c"
CLIENT_SECRET = "8e69e316b4984a5ea64291818ea9e4fb"
genius_url = "https://genius.com/albums/drake/nothing-was-the-same"
samples_list = []


def scrape_genius_url(genius_url):
    r = requests.get(genius_url)

    soup = BeautifulSoup(r.content, features="html.parser")

    song_links = []
    for link in soup.find_all(class_="u-display_block", href=True):
        song_links.append(link["href"])

    song_links = [i.replace("-lyrics", "-sample/samples") for i in song_links]
    for i in range(len(song_links)):
        if True:
            r = requests.get(song_links[i])
            if r.status_code == 200:
                song_samples_page = BeautifulSoup(r.content, "html.parser")
                song_relationships = song_samples_page.find_all(
                    class_="RelationshipListshared__RelationshipListSection-sc-1ulnidt-2 dBbpTG"
                )

                if (song_relationships is None) or (len(song_relationships) < 2):
                    continue
                else:
                    song_relationships = song_relationships[0]

                song_samples = song_relationships.find_all(
                    class_="SongCard__CardContents-sc-1bjj0ja-2 jLGCix"
                )

                for j in song_samples:
                    samples_list.append(
                        {
                            "song": j.contents[0].contents[0].get_text().strip(),
                            "artist": j.contents[1].contents[0].get_text().strip(),
                        }
                    )


def get_album_info():
    r = requests.get(genius_url)

    soup = BeautifulSoup(r.content, features="html.parser")
    album_title = (
        soup.find("li", {"class": "breadcrumb breadcrumb-current_page"})
        .find(itemprop="name")
        .get_text()
    )
    album_artist = soup.find(
        class_="header_with_cover_art-primary_info-primary_artist"
    ).get_text()

    return album_title, album_artist


def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"

    auth_response = requests.post(
        auth_url,
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {token}".format(token=access_token),
    }
    return access_token, headers


def get_audio_features(track_id, headers):
    BASE_URL = "https://api.spotify.com/v1/"
    r = requests.get(BASE_URL + "audio-features/" + track_id, headers=headers)
    print(r.json())


def create_playlist(album, artist):
    playlist_name = f"Samples in {album} by {artist}"
    sp.user_playlist_create(USER_ID, name=playlist_name)
    return playlist_name


def get_track_id():
    track_ids = []
    print(len(samples_list))
    for i in range(len(samples_list)):
        results = sp.search(
            q=f"{samples_list[i]['song']} {samples_list[i]['artist']} ",
            limit=5,
            type="track",
        )

        if results["tracks"]["total"] == 0:
            continue
        else:
            for j in range(len(results["tracks"]["items"])):
                aux_artist_a = results["tracks"]["items"][j]["artists"][0]["name"]
                aux_artist_b = samples_list[i]["artist"]
                aux_song_a = results["tracks"]["items"][j]["name"]
                aux_song_b = samples_list[i]["song"]

                aux_artist_a = aux_artist_a.lower()
                aux_artist_b = aux_artist_b.lower()
                aux_song_a = aux_song_a.lower()
                aux_song_b = aux_song_b.lower()
                if (round(sm(None, aux_artist_a, aux_artist_b).ratio(), 1) >= 0.9) and (
                    round(sm(None, aux_song_a, aux_song_b).ratio(), 1) >= 0.9
                ):
                    track_ids.append(
                        results["tracks"]["items"][j]["id"]
                    )

                    break

    return track_ids


def get_playlist_id(playlist_name):
    playlist_id = ""
    playlists = sp.user_playlists(USER_ID)
    for playlist in playlists["items"]:  # iterate through playlists I follow
        if playlist["name"] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist["id"]
    print("Got Playlist ID.")
    return playlist_id


# access_token, headers = get_spotify_token()


track_id = "3tnKGcCjPenqCCcffVz77U?si=fc03219a7cfd4888"

# get_audio_features(track_id, headers)
scope = "playlist-modify-public"
token = util.prompt_for_user_token(
    USER_ID,
    scope,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:8888/callback",
)

sp = spotipy.Spotify(auth=token)
album, artist = get_album_info()

playlist_name = create_playlist(album, artist)

scrape_genius_url(genius_url)
[print(i) for i in samples_list]

samples_id = get_track_id()
# get_track_id()
# [print(i) for i in samples_id]

sp.user_playlist_add_tracks(USER_ID, get_playlist_id(playlist_name), samples_id)

# [print(i) for i in samples_list]
