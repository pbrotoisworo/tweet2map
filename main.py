import tweepy
import sys
import argparse
from configparser import ConfigParser
import geopandas as gpd
import numpy as np
import pandas as pd
import pickle
import os
import traceback

from src.SqlManagement import Tweet2MapDatabaseSQL, LocationDatabaseSQL
from src.CheckConfig import check_for_valid_config
from src.ArgparseProcessing import argparse_config, argparse_generate_flags, argparse_processing
from src.ConnectTwitter import connect_to_twitter
from src.LoadTweets import load_tweets
from src.CheckDuplicateTweets import check_duplicate_tweets
from src.TweetParse import TweetParse
from src.AddNewLocation import add_new_location
from src.SpatialJoin import spatial_join
from src.CacheProcessing import cache_processing

def Tweet2Map():
    """
    Main function to run script
    """
    # Define work directory
    workspace = os.path.dirname(sys.argv[0])

    CONFIG_PATH = os.path.join(workspace, 'config.ini')
    CACHE_PATH = os.path.join(workspace, 'tweet_cache.pkl')

    # Check for valid config file and load
    config = check_for_valid_config(CONFIG_PATH, workspace=workspace)
    
    # Define CLI flags and parse inputs
    parser = argparse.ArgumentParser(description='Tweet2Map 1.0')
    parser = argparse_generate_flags(parser=parser)
    args = parser.parse_args()
    args = vars(args)

    # Process arguments
    argparse_return = argparse_processing(args=args, config=CONFIG_PATH)
    tweepy_params = argparse_return['tweepy_params']
    shp_path = argparse_return['shp_path']
    inc_database_path = argparse_return['inc_database_path']
    loc_database_path = argparse_return['loc_database_path']
    process_tweets = args['p']

    # Connect to Tweepy
    api = connect_to_twitter(consumer_key=tweepy_params['consumer_key'],
                             consumer_secret=tweepy_params['consumer_secret'],
                             access_token=tweepy_params['access_token'],
                             access_secret=tweepy_params['access_secret'])

    # Load Tweets
    tweets = load_tweets(api=api, screen_name='mmda', count=200)
    incoming_tweets = [tweet for tweet in reversed(tweets) if 'MMDA ALERT' in tweet.full_text]

    # Load SQL Database
    database_sql = Tweet2MapDatabaseSQL(sql_database_file=inc_database_path)
    recent_tweet_ids = database_sql.get_newest_tweet_ids(count=500)

    # Write to CSV if arg
    if args['csv_out_path']:
        csv_out_path = args['csv_out_path']
        file_extension = os.path.basename(csv_out_path)
        assert csv_out_path.endswith('.csv'), f'Invalid file extension in "{file_extension}". Must end in ".csv"'
        print('Writing CSV file:', csv_out_path)
        database_sql.convert_database_to_csv(csv_out_path)
        sys.exit()

    # Load cache for duplicate checking
    tweets_for_processing = []
    if os.path.exists(CACHE_PATH):
        
        # If cache exists load the file and combine with existing tweets
        with open(CACHE_PATH, 'rb') as f:
            tweet_cache = pickle.load(f)
        
        # Get IDs from cached and new tweets
        existing_cache_ids = [tweet.id_str for tweet in tweet_cache]
        incoming_tweet_ids = [tweet.id_str for tweet in incoming_tweets]
        
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

    if not process_tweets:
        # Download only and store to cache for later processing then exit
        cache_processing(cache_path=CACHE_PATH,
                         recent_processed_ids=recent_tweet_ids,
                         tweets=tweets_for_processing)
        sys.exit()
    
    # Load last n tweets to check for duplicates
    latest_tweet_ids = database_sql.get_newest_tweet_ids(count=200)

    # Load Locations
    location_sql = LocationDatabaseSQL(sql_database_file=loc_database_path)
    location_dict, location_accuracy_dict = location_sql.get_location_dictionary()

    # Process tweets
    process_counter = 0
    tweet_list = []  # Store processed tweets in list
    for tweet in tweets_for_processing:
        if 'MMDA ALERT' in tweet.full_text: # tweet.id_str not in existing_cache_ids:
            if tweet.id_str in recent_tweet_ids:
                print('Duplicate Data! Skipping to next tweet.')
                checkDuplicate = True
                continue
            else:
                tweet_text = tweet.full_text.upper()
                tweet_text = tweet_text.replace('  ', ' ')

                # Create TweetParse object then parse tweet
                twt = TweetParse(tweet)

                # Each individual tweet into a dict. Each unique dict will be appended to a list
                tweet_dict = {}
                tweet_dict['Tweet'] = twt.tweet_text
                tweet_dict['Date'] = twt.date
                tweet_dict['Time'] = twt.time
                tweet_dict['Source'] = twt.source
                tweet_dict['Location'] = twt.location
                tweet_dict['Direction'] = twt.direction
                tweet_dict['Type'] = twt.incident_type
                tweet_dict['Involved'] = twt.participants
                tweet_dict['Lanes_Blocked'] = twt.lanes_blocked
                tweet_list.append(tweet_dict)

    # Add locations
    for idx, item in enumerate(tweet_list):

        # While loop will keep repeating until a valid choice is made with the unknown location
        # while loop handling
        bool_location_added = False
        bool_user_reset = False
        bool_location_confirmed = False
        while not bool_location_added:
            try:
                if bool_user_reset:
                    # User reset due to revised name
                    location = location_revised
                    bool_user_reset = False
                elif bool_location_confirmed:
                    location = results_location
                else:
                    location = item['Location']

                tweet_text = item['Tweet']
                tweet_latitude = location_dict[location].split(',')[0]
                tweet_list[idx]['Latitude'] = tweet_latitude
                tweet_longitude = location_dict[location].split(',')[1]
                tweet_list[idx]['Longitude'] = tweet_longitude
                tweet_location_accuracy = location_accuracy_dict[location]
                tweet_list[idx]['High_Accuracy'] = tweet_location_accuracy

                print('---------------------------------------------------------------')
                print(f'Tweet {idx} of {len(tweet_list)}')
                print('Tweet:', tweet_text)
                print('Date:', item['Date'])
                print('Time:', item['Time'])
                print('URL:', item['Source'])
                print('Location:', location)
                print('Latitude:', tweet_latitude)
                print('Longitude:', tweet_longitude)
                print('High Accuracy:', tweet_list[idx]['High_Accuracy'])
                print('Direction:', item['Direction'])
                print('Incident Type:', item['Type'])
                print('Participants:', item['Involved'])
                print('Lanes Involved:', item['Lanes_Blocked'])
                process_counter += 1
                bool_location_added = True          

            except KeyError as e:
                
                print('---------------------------------------------------------------')
                print(f'Tweet {idx} of {len(tweet_list)}')
                print(f'New location detected! "{location}" is not recognized.')
                print(f'\nTweet: {tweet_text}')
                print(f'\nChoose an option from the list:')
                print('1 - Add new location and new coordinates (HIGH ACCURACY)')
                print('2 - Add new location and new coordinates (LOW ACCURACY)')
                print(f'3 - Add new location based on existing coordinates')
                print(f'4 - Fix location name')
                print(f'5 - Set location coordinates as invalid (0,0)')
                print(f'6 - Stop processing locations and exit\n')

                user_input_choice = str(input('Enter number to proceed:'))
                
                # Give user option to stop processing at current location
                # Tweet database is not updated yet, however location base is updated and will
                # allow the user to resume processing from their current position
                if user_input_choice == '6':
                    database_sql.close_connection()
                    location_sql.close_connection()
                    sys.exit()

                results = add_new_location(user_input_choice=user_input_choice,
                                           location=location,
                                           location_dict=location_dict,
                                           location_accuracy_dict=location_accuracy_dict,
                                           sql_object=location_sql)

                # results indexing
                # results[0] is location
                # results[1] is coordinates
                # results[2] is location_dict
                # reuslts[3] is location_accuracy_dict
                # reuslts[4] is bool_high_accuracy

                if results == 'BREAK':
                    continue
                if results[0] == 'REVISED':
                    bool_user_reset = True
                    location_revised = results[1]
                    continue
                    
                results_location = results[0]
                results_coords = results[1]
                tweet_latitude = results[1].split(',')[0]
                tweet_longitude = results[1].split(',')[1]
                location_dict = results[2]
                location_accuracy_dict = results[3]
                bool_high_accuracy = results[4]
                bool_location_confirmed = True
                continue

    # Spatial Join
    df = pd.DataFrame(tweet_list)
    df['Longitude'].replace(to_replace='None', value='0', inplace=True)
    df['Latitude'].replace(to_replace='None', value='0', inplace=True)
    df['Longitude'] = df['Longitude'].astype('float64')
    df['Latitude'] = df['Latitude'].astype('float64')
    df = spatial_join(df_input=df, shapefile=shp_path)

    print(f'\n{process_counter} new tweets added to database')

    # Update incident database
    for row in df.iterrows():
        database_sql.insert(row)

    # Close SQL connection
    database_sql.close_connection()
    location_sql.close_connection()

    # Delete cache if exists
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)

if __name__ == '__main__':
    
    # Run script
    Tweet2Map()