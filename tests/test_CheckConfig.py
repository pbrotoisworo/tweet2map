from src.ArgparseProcessing import argparse_config
from configparser import ConfigParser
import shutil
import os
import sys
import pytest
    
# Prepare config file for tests
global TEST_CONFIG_PATH
TESTS_DIR = os.path.dirname(__file__)
TEST_CONFIG_TEMPLATE = os.path.join(TESTS_DIR, 'test_config_template.ini')
TEST_CONFIG_PATH = os.path.join(TESTS_DIR, 'test_config.ini')
assert os.path.exists(TEST_CONFIG_TEMPLATE), f'Template file {TEST_CONFIG_TEMPLATE} not detected. Detected files: {os.listdir(TESTS_DIR)}'
shutil.copy(src=TEST_CONFIG_TEMPLATE, dst=TEST_CONFIG_PATH)


def test_argparse_inc_database_path():
    """
    Test incident database input
    """
    
    section = 'software'
    arg = r'test_data\data.sqlite'
    arg_type = 'database_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'database_path not updated in config file'
    assert actual == expected, message

def test_argparse_loc_database_path_string():
    """
    Test location database input
    """
    
    section = 'software'
    arg = r'test_data\locations.sqlite'
    arg_type = 'locations_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'locations_path not updated in config file'
    assert actual == expected, message
    
def test_argparse_shp_path_string():
    """
    Test shapefile path input
    """
    
    section = 'software'
    arg = r'test_data\boundary_ncr.shp'
    arg_type = 'shp_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'shp_path not updated in config file'
    assert actual == expected, message
    
@pytest.mark.xfail
def test_argparse_shp_path_string_fail():
    """
    Test shapefile path input
    """
    
    section = 'software'
    arg = r'test_data\boundary_ncr.shp.fail'
    arg_type = 'shp_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'shp_path not updated in config file'
    assert actual == expected, message
    
@pytest.mark.xfail
def test_argparse_loc_database_path_string_fail():
    """
    Test location database input
    """
    
    section = 'software'
    arg = r'test_data\locations.sqlite.fail'
    arg_type = 'locations_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'locations_path not updated in config file'
    assert actual == expected, message
    
@pytest.mark.xfail
def test_argparse_inc_database_path_fail():
    """
    Test incident database input
    """
    
    section = 'software'
    arg = r'test_data\data.sqlite.fail'
    arg_type = 'database_path'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'database_path not updated in config file'
    assert actual == expected, message
    
def test_argparse_tweepy_consumer_key():
    """
    Test Tweepy consumer key
    """
    
    section = 'tweepy'
    arg = 'TestConsumerKey1234'
    arg_type = 'consumer_key'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'Tweepy consumer token not updated in config file'
    assert actual == expected, message
    
def test_argparse_tweepy_consumer_secret():
    """
    Test Tweepy consumer secret
    """
    
    section = 'tweepy'
    arg = 'TestConsumerSecret5678'
    arg_type = 'consumer_secret'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'Tweepy consumer secret not updated in config file'
    assert actual == expected, message
    
def test_argparse_tweepy_access_token():
    """
    Test Tweepy access token
    """
    
    section = 'tweepy'
    arg = 'TestAccessToken90123'
    arg_type = 'access_token'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'Tweepy access token not updated in config file'
    assert actual == expected, message
    
def test_argparse_tweepy_access_secret():
    """
    Test Tweepy access token
    """
    
    section = 'tweepy'
    arg = 'TestAccessSecret4567'
    arg_type = 'access_secret'
    
    kwargs = dict()
    kwargs['arg'] = arg
    kwargs['section'] = section
    kwargs['arg_type'] = arg_type
    kwargs['config_path'] = TEST_CONFIG_PATH
    _ = argparse_config(**kwargs)
    
    # Assert config file is modified
    config = ConfigParser()
    config.read(TEST_CONFIG_PATH)
    actual = config.get(section, arg_type)
    expected = arg
    message = 'Tweepy access secret not updated in config file'
    assert actual == expected, message