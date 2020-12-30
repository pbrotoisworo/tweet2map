from src.SqlManagement import Tweet2MapDatabaseSQL, LocationDatabaseSQL
import os
import pytest

TESTS_DIR = os.path.dirname(__file__)
PATH_TEST_INC_DATABASE = os.path.join(TESTS_DIR, r'test_data\\data.sqlite')
PATH_TEST_LOCATION_DATABASE = (TESTS_DIR, r'test_data\\locations.sqlite')
num_latest_tweets = 50

def test_inc_db_sql_init():
    """
    Test initialization of SQL management class
    """
    
    database_sql = Tweet2MapDatabaseSQL(sql_database_file=PATH_TEST_INC_DATABASE, num_latest_tweets=num_latest_tweets, verbose=True)
    
    actual_row_count = database_sql.row_count
    expected_row_count = 100
    assert expected_row_count == actual_row_count, f'total rows: {actual_row_count}'
    
    actual_cols = database_sql.columns
    expected_cols = ['Date', 'Time', 'City', 'Location', 'Latitude' ,'Longitude', 'High_Accuracy',
                     'Direction', 'Type', 'Lanes_Blocked', 'Involved', 'Tweet', 'Source']
    assert len(expected_cols) == len(actual_cols), f'Unexpected number of columns. Input columns are: {database_sql.columns}'

def test_inc_db_sql_newest_tweet_ids():
    """
    Test getting latest tweet IDs from SQL database
    """
    database_sql = Tweet2MapDatabaseSQL(sql_database_file=PATH_TEST_INC_DATABASE, num_latest_tweets=num_latest_tweets, verbose=True)
    latest_ids = database_sql.get_newest_tweet_ids()
    message = f'Number of rows to check does not match the count of the return of get_newest_tweet_ids()'
    assert num_latest_tweets == len(latest_ids), message