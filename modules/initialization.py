<<<<<<< HEAD
# initialization scripts for Tweet2Map
from configparser import ConfigParser
import tweepy
from modules.RunConfig import *
import csv
import traceback
import time


def initialization_tweepy_connect(max_connect_attempts=4,
                                  timeout_length=15,
                                  input_consumer_key=None,
                                  input_consumer_secret=None,
                                  input_access_token=None,
                                  input_access_secret=None):
    """
    Connect to Twitter and load tweets
    Keeps connecting to Tweepy service
    If max_connect_attempts set to None it will attempt forever
    """

    connect_attempts = 0
    userConnection = False
    show_error = True

    while userConnection == False:
        try:
            # Tweepy Settings
            consumer_key = input_consumer_key
            consumer_secret = input_consumer_secret
            access_token = input_access_token
            access_secret = input_access_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            api = tweepy.API(auth)
            tweets = api.user_timeline(screen_name="mmda", count=200, include_rts=False)
            # If it can connect, then get out of the while loop
            userConnection = True
        except tweepy.TweepError as e:

            if show_error == True:
                print(e.reason, '\n')
                print('Connection attempt failed!\n')
                show_error = False

            if max_connect_attempts != None and isinstance(max_connect_attempts, int):
                connect_attempts += 1
                if connect_attempts == max_connect_attempts:
                    print('\nPlease check your connection.')
                    print('Terminating script.')
                    tweets = []

            print('Retrying in {} seconds'.format(timeout_length))
            time.sleep(timeout_length)

    return tweets


def initialization_check_duplicate(tweet_database=None, max_tweets=200):
    """
    Load last set of tweets to check for duplicates
    """
    lstDuplicateCheck = []

    try:
        with open(tweet_database, 'r', newline='') as CsvFile:
            reader = csv.reader(CsvFile)

            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    # print('Duplicate check initialized')
                    break

    except FileNotFoundError:
        print('CSV file not detected. Creating new CSV file')
        with open(tweet_database, 'x', newline='') as CsvFile:
            # reader = csv.reader(CsvFile)
            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    break

    return lstDuplicateCheck
=======
# initialization scripts for Tweet2Map
from configparser import ConfigParser
import tweepy
from modules.RunConfig import *
import csv
import traceback
import time


def initialization_tweepy_connect(max_connect_attempts=4,
                                  timeout_length=15,
                                  input_consumer_key=None,
                                  input_consumer_secret=None,
                                  input_access_token=None,
                                  input_access_secret=None):
    """
    Connect to Twitter and load tweets
    Keeps connecting to Tweepy service
    If max_connect_attempts set to None it will attempt forever
    """

    connect_attempts = 0
    userConnection = False
    show_error = True

    while userConnection == False:
        try:
            # Tweepy Settings
            consumer_key = input_consumer_key
            consumer_secret = input_consumer_secret
            access_token = input_access_token
            access_secret = input_access_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            api = tweepy.API(auth)
            tweets = api.user_timeline(screen_name="mmda", count=200, include_rts=False)
            # If it can connect, then get out of the while loop
            userConnection = True
        except tweepy.TweepError as e:

            if show_error == True:
                print(e.reason, '\n')
                print('Connection attempt failed!\n')
                show_error = False

            if max_connect_attempts != None and isinstance(max_connect_attempts, int):
                connect_attempts += 1
                if connect_attempts == max_connect_attempts:
                    print('\nPlease check your connection.')
                    print('Terminating script.')
                    tweets = []

            print('Retrying in {} seconds'.format(timeout_length))
            time.sleep(timeout_length)

    return tweets


def initialization_check_duplicate(tweet_database=None, max_tweets=200):
    """
    Load last set of tweets to check for duplicates
    """
    lstDuplicateCheck = []

    try:
        with open(tweet_database, 'r', newline='') as CsvFile:
            reader = csv.reader(CsvFile)

            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    # print('Duplicate check initialized')
                    break

    except FileNotFoundError:
        print('CSV file not detected. Creating new CSV file')
        with open(tweet_database, 'x', newline='') as CsvFile:
            # reader = csv.reader(CsvFile)
            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    break

    return lstDuplicateCheck
>>>>>>> 02fbe3340762954ee38b54461631d0e36a0878b4
