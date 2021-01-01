import sys
import tweepy
import re
import logging
from datetime import datetime, timedelta
import pickle
import os
from src.TweetParse import TweetParse

global tweets
TESTS_DIR = os.path.dirname(__file__)
test_tweepy_object = os.path.join(TESTS_DIR, 'test_data', 'tweepy_tweets.pickle')
with open(test_tweepy_object, 'rb') as handle:
    tweets = pickle.load(handle)
    
def test_tweetparse_strip_direction():
    """
    Test strip direction method of TweetParse
    """
    twt = TweetParse(tweets[59])
    test_text = 'MMDA ALERT: Vehicular accident at Commonwealth Doña Carmen EB involving taxi and AUV as of 8:25 PM. 1 lane occupied. MMDA on site. #mmda'.upper()
    
    actual = twt._strip_direction(text=test_text)
    expected = 'MMDA ALERT: Vehicular accident at Commonwealth Doña Carmen involving taxi and AUV as of 8:25 PM. 1 lane occupied. MMDA on site. #mmda'.upper()
    message = f'Assertion of strip direction failed. Expected: "{expected}". Actual: "{actual}"'
    assert actual == expected, message

def test_tweetparse_scenario1():
    """
    Test tweet scenario
    """
    twt = TweetParse(tweets[59])
    expected_tweet_text = 'MMDA ALERT: Vehicular accident at Commonwealth Doña Carmen EB involving taxi and AUV as of 8:25 PM. 1 lane occupied. MMDA on site. #mmda'.upper()
    expected_location = 'COMMONWEALTH DONA CARMEN'
    expected_time = '8:25 PM'
    expected_date = '2020-12-28'
    expected_inc_type = 'VEHICULAR ACCIDENT'
    expected_participants = 'TAXI AND AUV'
    expected_source = 'https://twitter.com/mmda/status/1343535465090088961'
    expected_direction = 'EB'
    expected_lanes_blocked = '1'
    
    actual_tweet_text = twt.tweet_text
    message = f'TweetParse.tweet_text does not match {expected_tweet_text}'
    assert expected_tweet_text == actual_tweet_text, message
    
    actual_location = twt.location
    message = f'TweetParse.location returned "{actual_location}". This does not match expected location "{expected_location}"'
    assert expected_location == actual_location, message
    
    actual_time = twt.time
    message = f'TweetParse.time returned "{actual_time}". This does not match expected time "{expected_time}"'
    assert expected_time == actual_time, message
    
    actual_date = twt.date
    message = f'TweetParse.date returned "{actual_date}". This does not match expected date "{expected_date}"'
    assert expected_date == actual_date, message
    
    actual_inc_type = twt.incident_type
    message = f'TweetParse.incident_type returned "{actual_inc_type}". This does not match expected date "{expected_inc_type}"'
    assert expected_inc_type == actual_inc_type, message
    
    actual_participants = twt.participants
    message = f'TweetParse.participants returned "{actual_participants}". This does not match expected participants "{expected_participants}"'
    assert expected_participants == actual_participants, message
    
    actual_source = twt.source
    message = f'TweetParse.source returned "{actual_source}". This does not match expected source "{expected_source}"'
    assert expected_source == actual_source, message
    
    actual_direction = twt.direction
    message = f'TweetParse.direction returned "{actual_direction}". This does not match expected direction "{expected_direction}"'
    assert expected_direction == actual_direction, message
    
    actual_lanes_blocked = twt.lanes_blocked
    message = f'TweetParse.lanes_blocked returned "{actual_lanes_blocked}". This does not match expected lanes blocked "{expected_lanes_blocked}"'
    assert expected_lanes_blocked == actual_lanes_blocked, message
