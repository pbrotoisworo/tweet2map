import tweepy
import sys

def load_tweets(api, screen_name, count):
    """Load tweets using Tweepy API"""

    try:
        tweets = api.user_timeline(screen_name='mmda', count=200, include_rts=False, tweet_mode='extended')
    except Exception as e:
        print(e)
        print('Cannot load tweets')
        sys.exit()
        
    if len(tweets) == 0:
        print('No Tweets were downloaded')
        sys.exit()
    else:
        return tweets
