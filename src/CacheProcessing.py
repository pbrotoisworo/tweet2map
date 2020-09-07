import pickle
import sys
import os

def cache_processing(cache_path, recent_processed_ids, tweets):
    """Cache processing for Tweets"""
    # Download into cache for later processing
    #TODO: this still adds to cache even if the processing was just run. double check dup checks
    if not os.path.exists(cache_path):
        # If does not exist create PKL file
        # No filtering required because it is already filtered
        cached_tweets = []
        for tweet in tweets:
            cached_tweets.append(tweet)
        # for tweet in tweets:
        #     if tweet.id_str not in recent_processed_ids:
        #         # Cross check with recent processed IDs in incident database before appending
        #         cached_tweets.append(tweet)
        cache_size = len(cached_tweets)
        print('Creating new cache')
        print('Current cache size:', cache_size)

        with open(cache_path, 'wb') as f:
            pickle.dump(cached_tweets, f)
        
    else:
        # If exists, load cache
        with open(cache_path, 'rb') as f:
            try:
                cached_tweets = pickle.load(f)
            except EOFError:
                print('EOF error with PKL file. Cache might be empty')
                print('Closing software')
                sys.exit()

        cached_ids = [cached_tweet.id_str for cached_tweet in cached_tweets]
        added_cache_counter = 0

        for tweet in tweets:
            # Before adding to the cache, check existing id_str in cache and recent processed IDs in incident database
            if ((tweet.id_str not in cached_ids) and (tweet.id_str not in recent_processed_ids)):
                cached_tweets.append(tweet)
                added_cache_counter += 1

        if not added_cache_counter:
            print('No new tweets detected')
            return
        
        cache_size = len(cached_tweets)

        with open(cache_path, 'wb') as f:
            pickle.dump(cached_tweets, f)

        # print(f'Reduced to {num_incoming_tweets} tweets after filtering. Added {added_cache_counter} to cache.')
        print(f'Added {added_cache_counter} new tweets to cache')
        print('Current cache size:', cache_size)

    return