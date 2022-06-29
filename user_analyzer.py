from spotipy.oauth2 import SpotifyClientCredentials
from unicodedata import name
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import tweepy
import time
import os


def get_user_tracklist(username: str):
    CONSUMER_KEY = os.getenv('TWEEPY_CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('TWEEPY_CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('TWEEPY_ACCESS_KEY')
    ACCESS_SECRET = os.getenv('TWEEPY_ACCESS_SECRET')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=username,
                               count=200,
                               include_rts=False,
                               tweet_mode='extended'
                               )

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=username,
                                   count=200,
                                   include_rts=False,
                                   max_id=oldest_id - 1,
                                   tweet_mode='extended'
                                   )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('Tweets obtenidos del usuario hasta ahora: {}'.format(len(all_tweets)))

    tracks = []
    albums = []

    print(f"Conseguidos {len(all_tweets)} tweets del usuario")
    for tweet in all_tweets:
        if(tweet.entities["urls"]):
            if("spotify" in tweet.entities["urls"][0]["expanded_url"]):
                if("album" in tweet.entities["urls"][0]["expanded_url"]):
                    print("Album encontrado: " +
                          tweet.entities["urls"][0]["expanded_url"])
                    albums.append(tweet.entities["urls"][0]["expanded_url"])
                elif("track" in tweet.entities["urls"][0]["expanded_url"]):
                    print("Track encontrado: " +
                          tweet.entities["urls"][0]["expanded_url"])
                    tracks.append(tweet.entities["urls"][0]["expanded_url"])

    print(
        f"Albums encontrados en los ultimos {len(all_tweets)} tweets: {len(albums)}")
    print(
        f"Tracks encontrados en los ultimos {len(all_tweets)} tweets: {len(tracks)}")

    return len(all_tweets), tracks
