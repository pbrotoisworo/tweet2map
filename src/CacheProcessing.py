import pickle
import sys
import os

def cache_processing(download_arg, cache_path, recent_processed_ids, tweets):
    """Cache processing for Tweets"""

    if download_arg:
        # Download into cache for later processing
        if not os.path.exists(cache_path):
            # If does not exist create PKL file
            tweepy_object_list = []
            for tweet in tweets:
                if tweet.id_str not in recent_processed_ids:
                    # Cross check with recent processed IDs in incident database before appending
                    tweepy_object_list.append(tweet)
            cache_size = len(tweepy_object_list)
            print('Current cache size:', cache_size)

            with open(cache_path, 'wb') as f:
                pickle.dump(tweepy_object_list, f)
            
        else:
            # If exists, load cache
            with open(cache_path, 'rb') as f:
                tweepy_object_list = pickle.load(f)
            existing_ids = [existing_tweet.id_str for existing_tweet in tweepy_object_list]
            added_cache_counter = 0
            for tweet in tweets:
                # Before adding to the cache, check existing id_str in cache and recent processed IDs in incident database
                if (tweet.id_str not in existing_ids) and (tweet.id_str not in recent_processed_ids):
                    tweepy_object_list.append(tweet)
                    added_cache_counter += 1
            cache_size = len(tweepy_object_list)
            print(f'Added {added_cache_counter} to cache')
            print('Current cache size:', cache_size)
        sys.exit()
    else:
        pass
    return