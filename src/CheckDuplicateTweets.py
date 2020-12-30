import pickle
import os

def check_duplicate_tweets(cache_path, incoming_tweets, recent_tweet_ids):
    """
    Load last set of tweets to check for duplicates
    """

    # Load cache for duplicate checking
    tweets_for_processing = []
    if os.path.exists(cache_path):
        
        # If cache exists load the file and combine with existing tweets
        with open(cache_path, 'rb') as f:
            tweet_cache = pickle.load(f)
        
        # Get IDs from cached and new tweets
        existing_cache_ids = [tweet.id_str for tweet in tweet_cache]
        # incoming_tweet_ids = [tweet.id_str for tweet in incoming_tweets]
        
        tweets_for_processing += tweet_cache
    
        # Add incoming tweets but check if they exist first in cache
        for tweet in incoming_tweets:
            if tweet.id_str not in existing_cache_ids:
                tweets_for_processing.append(tweet)
    else:
        # No cache. So add all incoming tweets
        tweets_for_processing += incoming_tweets

    # Remove incoming tweets that are already in the incident database
    for idx, tweet in enumerate(tweets_for_processing):
        if tweet.id_str in recent_tweet_ids:
            del tweets_for_processing[idx]

    return tweets_for_processing