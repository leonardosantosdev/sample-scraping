import spotipy


def spotify_auth(user_id, client_id, client_secret):
    scope = "playlist-modify-public"
    token = spotipy.util.prompt_for_user_token(
        user_id,
        scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
    )

    return spotipy.Spotify(auth=token)
