from src.SqlManagement import Tweet2MapDatabaseSQL, LocationDatabaseSQL
import os
import pytest
import shutil
import pandas as pd
import time

global PATH_TEST_INC_DATABASE
TESTS_DIR = os.path.dirname(__file__)
PATH_TEMPLATE_INC_DATABASE = os.path.join(TESTS_DIR, 'test_data', 'data.sqlite')
PATH_TEST_INC_DATABASE = os.path.join(TESTS_DIR, 'test_data', 'data_test.sqlite')
PATH_TEST_LOCATION_DATABASE = os.path.join(TESTS_DIR, 'test_data', 'locations.sqlite')
PATH_TEST_CSV_OUTPUT = os.path.join(TESTS_DIR, 'test_data', 'output_csv.csv')
if os.path.exists(PATH_TEST_INC_DATABASE):
    os.remove(PATH_TEST_INC_DATABASE)
shutil.copy(src=PATH_TEMPLATE_INC_DATABASE, dst=PATH_TEST_INC_DATABASE)
num_latest_tweets = 50

@pytest.fixture
def inc_database():
    """
    Load an instance of the SQL database manager
    """
    return Tweet2MapDatabaseSQL(sql_database_file=PATH_TEST_INC_DATABASE, num_latest_tweets=num_latest_tweets, verbose=True)

def test_init_row_count(inc_database):
    expected = 100
    actual = inc_database.row_count
    assert expected == actual, 'Row count does not match'
    
def test_init_col_count(inc_database):
    expected = 13
    actual = len(inc_database.columns)
    assert expected == actual, 'Column count does not match'
    
def test_get_latest_tweet_ids(inc_database):
    expected = num_latest_tweets
    actual = len(inc_database.get_newest_tweet_ids())
    message = f'Count of latest tweets does not match. Expected is "{expected}". Received "{actual}"'
    assert expected == actual, message
    
def test_write_to_csv(inc_database):
    
    inc_database.convert_database_to_csv(PATH_TEST_CSV_OUTPUT)
    
    file_exists = os.path.exists(PATH_TEST_CSV_OUTPUT)
    message = f'Test CSV not detected at path "{PATH_TEST_CSV_OUTPUT}"'
    assert file_exists == True, message
    
def test_csv_row_count():
    
    df_test = pd.read_csv(PATH_TEST_CSV_OUTPUT)
    actual_csv_rows = len(df_test)
    expected_csv_rows = 100
    message = f'Test CSV not written properly. Expected row count is {expected_csv_rows}. Actual row count is {actual_csv_rows}.'
    assert expected_csv_rows == actual_csv_rows, message
    
def test_insert_to_database(inc_database):
    
    df = pd.DataFrame(columns=['Date', 'Time', 'City', 'Location', 'Latitude',
                               'Longitude', 'High_Accuracy', 'Direction', 'Type',
                               'Lanes_Blocked', 'Involved', 'Tweet', 'Source'])
    df.loc[0] = ['2015-05-01', '03:00 PM', 'Test City', 'JUNIPER AVENUE', '14.562570996429075',
                 '121.0700600595116', '1', '', 'VEHICULAR ACCIDENT', '1', 'CAR AND AUV',
                 'MMDA ALERT: VEHICULAR ACCIDENT AT JUNIPER AVENUE. TEST ROW.', 'https://www.twitter.com/mmda/1234567890']
    row = list(df.iterrows())[0]

    original = inc_database.count_rows()
    inc_database.insert(row)
    
    expected = 101
    actual = inc_database.count_rows()
    message = f'Failed assertion on inserting incident data to SQL table. Original row count is {original}. Expected row count is {expected}. Actual row count is {actual}'
    assert expected == actual, message