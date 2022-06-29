from time import sleep
import tweepy
import os
from spotipy_playlist_maker import create_playlist
from user_analyzer import get_user_tracklist


def retrieve_lastseen_id(file_name):
    f_read = open(file_name, 'r')
    lastseen_id = int(f_read.read().strip())
    f_read.close()
    return lastseen_id


def store_lastseen_id(lastseen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lastseen_id))
    f_write.close()
    return


def reply_to_tweets():
    last_seen_id = retrieve_lastseen_id(last_view_file_name)
    print('ID del ultimo tweet respondido: ', last_seen_id)

    mentions = api.mentions_timeline(
        since_id=last_seen_id,
        tweet_mode='extended'
    )

    for mention in reversed(mentions):
        print('Respondiendo a la mención ' +
              str(mention.id) + ' - ' + mention.full_text)
        print('Obteniendo detalles del usuario...')
        # Obteniendo detalles del usuario
        try:
            [n_tweets, tracks] = get_user_tracklist(mention.user.screen_name)
        except:
            print('Error al obtener detalles del usuario. Esperando 15 minutos...')
            sleep(900)
            return

        last_seen_id = mention.id
        store_lastseen_id(last_seen_id, last_view_file_name)
        print('Número de tweets analizados: ' + str(n_tweets))
        print('Número de tracks: ' + str(len(tracks)))
        print("Creando playlist...")

        # Creando playlist
        try:
            playlist_link = create_playlist(
                tracks=tracks, playlist_user=mention.user.screen_name, n_tweets=n_tweets)
        except:
            print("Error al crear playlist.")
            playlist_link = ""

        print('Respondiendo...', flush=True)
        if playlist_link != "no_tracks" and playlist_link != "":
            api.update_status("@" + mention.user.screen_name +
                              " Aquí está tu playlist basada en tus últimos " + str(n_tweets) + " tweets: \n " + playlist_link, in_reply_to_status_id=mention.id)
        elif playlist_link == "no_tracks":
            api.update_status("@" + mention.user.screen_name +
                              " No tienes ninguna cancion publicada en tus últimos " + str(n_tweets) + " tweets :(", in_reply_to_status_id=mention.id)
        else:
            api.update_status("@" + mention.user.screen_name +
                              " Ha ocurrido un error y he colapsao ", in_reply_to_status_id=mention.id)
        sleep(30)


if __name__ == '__main__':

    CONSUMER_KEY = os.getenv('TWEEPY_CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('TWEEPY_CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('TWEEPY_ACCESS_KEY')
    ACCESS_SECRET = os.getenv('TWEEPY_ACCESS_SECRET')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    last_view_file_name = 'last_seen.txt'
    last_seen_id = retrieve_lastseen_id(last_view_file_name)
    # mention_keyword = 'nap'

    while True:
        print('Refrescando menciones...')
        reply_to_tweets()
        sleep(20)
