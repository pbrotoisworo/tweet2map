import tweepy
import sys
import time

def connect_to_twitter(consumer_key, consumer_secret, access_token, access_secret, max_connect_attempts=5, timeout_length=15):
    """Connect to Twitter using credentials"""

    connect_attempts = 0
    userConnection = False

    while userConnection == False:
        try:
            # Tweepy Settings
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            api = tweepy.API(auth)
            userConnection = True
        except tweepy.TweepError as e:

            if max_connect_attempts != None and isinstance(max_connect_attempts, int):
                connect_attempts += 1
                if connect_attempts == max_connect_attempts:
                    print('\nPlease ensure connection to Twitter exists.')
                    print('Terminating script.')
                    sys.exit()

            print(e.reason, '\n')
            print(f'Retrying connection in {timeout_length} seconds...\n')
            time.sleep(timeout_length)

    return api