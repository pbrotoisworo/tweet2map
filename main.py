import tweepy
import sys
import argparse
from configparser import ConfigParser

from src.SqlManagement import Tweet2MapDatabaseSQL
from src.LocationManagement import LocationDatabaseSQL
from src.CheckConfig import check_for_valid_config
from src.ArgparseProcessing import argparse_tweepy
from src.ConnectTwitter import connect_to_twitter
from src.LoadTweets import load_tweets
from src.CheckDuplicateTweets import check_duplicate_tweets
from src.TweetParse import TweetParse


# Read unprocessed data


# Extract tweets


# Cross check with unprocessed data

if __name__ == '__main__':

    # Define work directory
    workspace = sys.argv[0]

    CONFIG_PATH = 'testconfig.ini'

    # Check for valid config file and load
    config = check_for_valid_config(CONFIG_PATH)

    # Define CLI inputs
    parser = argparse.ArgumentParser(description='Tweet2Map 1.0')
    cli_args = parser.add_argument_group('Arguments')
    cli_args.add_argument('-v', help='Verbose mode', action='store_true')
    cli_args.add_argument('-consumer_key', help='Twitter API consumer key')
    cli_args.add_argument('-consumer_secret', help='Twitter API consumer secret')
    cli_args.add_argument('-access_token', help='Twitter API access token')
    cli_args.add_argument('-access_secret', help='Twitter API access secret')
    cli_args.add_argument('-database', help='Database path')
    cli_args.add_argument('-shp_path', help='Shapefile path')
    cli_args.add_argument('-location')
    # Convert args to dict
    args = parser.parse_args()
    args = vars(args)

    # Process arguments
    tweepy_params = {}
    tweepy_params['consumer_key'] = argparse_tweepy(arg=args['consumer_key'], arg_type='consumer_key', config_path=CONFIG_PATH)
    tweepy_params['consumer_secret'] = argparse_tweepy(arg=args['consumer_secret'], arg_type='consumer_secret', config_path=CONFIG_PATH)
    tweepy_params['access_token'] = argparse_tweepy(arg=args['access_token'], arg_type='access_token', config_path=CONFIG_PATH)
    tweepy_params['access_secret'] = argparse_tweepy(arg=args['access_secret'], arg_type='access_secret', config_path=CONFIG_PATH)

    # Load Locations
    location_sql = LocationDatabaseSQL(sql_database_file=config.get('software', 'locations_path'))
    location_dict = location_sql.get_location_dictionary()
    # LOCATION_SQL.search_matching_location('EDSA GUADALUPE')

    # Connect to Tweepy
    api = connect_to_twitter(consumer_key=tweepy_params['consumer_key'],
                             consumer_secret=tweepy_params['consumer_secret'],
                             access_token=tweepy_params['access_token'],
                             access_secret=tweepy_params['access_secret'])

    # Load SQL Database
    database_sql = Tweet2MapDatabaseSQL(sql_database_file=config.get('software', 'database_path'))
    

    # Load Tweets
    tweets = load_tweets(api=api, screen_name='mmda', count=200)
    # Load last n tweets to check for duplicates
    latest_tweet_ids = database_sql.get_newest_tweet_ids(tweets=tweets, count=200)

    # Process tweets
    for tweet in reversed(tweets):
        if 'MMDA ALERT' in tweet.full_text:
            tweet_url = 'https://twitter.com/mmda/status/' + str(tweet.id_str)

            if tweet_url in latest_tweet_ids:
                print('Duplicate Data! Skipping to next tweet.')
                checkDuplicate = True
                continue
            else:
                tweet_text = tweet.full_text.upper()
                tweet_text = tweet_text.replace('  ', ' ')

                # Create TweetParse object then parse tweet
                twt = TweetParse(tweet)

                print('---------------------------------------------------------------')
                print(f'Tweet: {twt.tweet_text}')
                print(f'Date: {twt.date}')
                print(f'Time: {twt.time}')
                print(f'URL: {tweet_url}')
                print(f'Location: {twt.location}')
                print(f'Direction: {twt.direction}')
                print(f'Incident Type: {twt.incident_type}')
                print(f'Participants: {twt.participants}')
                print(f'Lanes Involved: {twt.lanes_blocked}')

            # Try to check location with the database. If does not exist, assign new coordinates
            while_loop_unknown_location = False
            while not while_loop_unknown_location:
                try:
                    tweetLatitude = location_dict[twt.location].split(',')[0]
                    tweetLongitude = location_dict[twt.location].split(',')[1]
                    print(f'Latitude: {tweetLatitude}')
                    print(f'Longitude: {tweetLongitude}')
                    # Location is already added. Set check states to true
                    checkLocationAdded = True
                    checkUserLocationChoice = True
                    while_loop_unknown_location = True
                except KeyError:
                    while_loop_unknown_location = True

                

    database_sql.close_connection()