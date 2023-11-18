import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm


class SampleScraping():
    def __init__(self, user_id, genius_url, sp) -> None:
        self.user_id = user_id
        self.genius_url = genius_url
        self.sp = sp
        self.samples_list = []

    def create_samples_playlist(self):
        playlist_name = self._create_playlist()
        self._scrape_genius_url()
        samples_id = self._get_track_id()

        self.sp.user_playlist_add_tracks(
            self.user_id,
            self._get_playlist_id(playlist_name),
            samples_id
        )

    def _get_album_info(self):
        try:
            r = requests.get(self.genius_url)
            r.raise_for_status()
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

        except Exception as e:
            raise e

    def _create_playlist(self):
        album, artist = self._get_album_info()
        playlist_name = f"Samples in {album} by {artist}"
        self.sp.user_playlist_create(self.user_id, name=playlist_name)
        return playlist_name

    def _scrape_genius_url(self):
        try:
            r = requests.get(self.genius_url)
            soup = BeautifulSoup(r.content, features="html.parser")

            song_links = []
            for link in soup.find_all(class_="u-display_block", href=True):
                song_links.append(link["href"])

            song_links = [i.replace("-lyrics", "-sample/samples") for i in song_links]
            for i in range(len(song_links)):
                if True:
                    try:
                        r = requests.get(song_links[i])
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
                            self.samples_list.append(
                                {
                                    "song": j.contents[0].contents[0].get_text().strip(),
                                    "artist": j.contents[1].contents[0].get_text().strip(),
                                }
                            )
                    except Exception as e:
                        raise e
        except Exception as e:
            raise e

    def _get_track_id(self):
        track_ids = []
        for i in range(len(self.samples_list)):
            results = self.sp.search(
                q=f"{self.samples_list[i]['song']} {self.samples_list[i]['artist']} ",
                limit=5,
                type="track",
            )

            if results["tracks"]["total"] == 0:
                continue
            else:
                for j in range(len(results["tracks"]["items"])):
                    aux_artist_a = results["tracks"]["items"][j]["artists"][0]["name"]
                    aux_artist_b = self.samples_list[i]["artist"]
                    aux_song_a = results["tracks"]["items"][j]["name"]
                    aux_song_b = self.samples_list[i]["song"]

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

    def _get_playlist_id(self, playlist_name):
        playlist_id = ""
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists["items"]:  # iterate through playlists I follow
            if playlist["name"] == playlist_name:  # filter for newly created playlist
                playlist_id = playlist["id"]
        return playlist_id
