from __future__ import print_function
from spotipy.oauth2 import SpotifyOAuth
from pandas import array
import spotipy
import spotipy.util as util
import os
from datetime import date


def create_playlist(tracks: array, playlist_user: str, n_tweets: int):
    bot_user = os.getenv("SPOTIPY_BOT_USER")
    scope = 'user-library-read playlist-modify-public playlist-read-private playlist-modify-private'
    token = util.prompt_for_user_token(bot_user, scope)

    track_ids = []
    for track in tracks:
        track_ids.append(track.split("/")[-1].split("?")[0])
    track_ids = list(set(track_ids))
    print("track ids: ", track_ids)

    if token:
        if len(track_ids) <= 0:
            print("No tracks to add to playlist")
            return "no_tracks"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_APP_CLIENT_ID",
                                                       client_secret="YOUR_APP_CLIENT_SECRET",
                                                       redirect_uri="YOUR_APP_REDIRECT_URI",
                                                       scope="user-library-read"))
        sp.trace = False

        today = date.today()
        playlist_name = "Tweetlist de " + playlist_user + \
            " " + today.strftime("%d-%m-%Y")
        playlist_desc = "Playlist compuesta por los ultimos " + \
            str(n_tweets) + " tweets de " + playlist_user

        playlist = sp.user_playlist_create(user=bot_user, name=playlist_name,
                                           public=True, collaborative=False, description=playlist_desc)

        print("Id de la playlist: ", playlist.get("id"))

        sp.user_playlist_add_tracks(
            user=bot_user, tracks=track_ids, playlist_id=playlist.get("id"))
        print("Playlist de prueba creada")
        return playlist.get("external_urls").get("spotify")
    else:
        print("Can't get token for ", bot_user)
        return "error_token"
