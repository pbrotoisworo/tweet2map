from configparser import ConfigParser
import os


def check_for_valid_config(config_path):
    """Checks for valid config file and if it contains required settings.
    If it doesn't exist, create one using default parameters."""

    parser = ConfigParser()
    parser.read(config_path)
    
    if not os.path.exists(config_path):
        print('Config file not found. Creating config file.')
        parser['tweepy'] = {'consumer_key': '', 'consumer_secret': '', 'access_token': '', 'access_secret': ''}
        parser['software'] = {'database_path': r'data\data.sql', 'shp_path': r'shapefiles\boundary_ncr.shp'}
        parser.write(open(config_path, 'w'))
    else:
        # Check software_config section
        software_config = dict(parser.items('software'))
        software_config_keys = software_config.keys()
        # Check for valid keys
        assert (('database_path' in software_config_keys) and ('shp_path' in software_config_keys) and
                ('locations_path' in software_config_keys)), 'Invalid config file. Expected software parameters: database_path, shp_path, locations_path'

        # Check tweepy section
        tweepy_config = dict(parser.items('tweepy'))
        tweepy_config_keys = tweepy_config.keys()
        # Check for valid keys
        assert (('consumer_key' in tweepy_config_keys) and ('consumer_secret' in tweepy_config_keys)
        and ('access_token' in tweepy_config_keys) and ('access_secret' in tweepy_config_keys)), 'Invalid config file. Expected tweepy parameters: consumer_key, consumer_secret, access_token, access_secret'
        
    # Check for existance
    database_path = parser.get('software', 'database_path')
    shp_path = parser.get('software', 'shp_path')
    locations_path = parser.get('software', 'locations_path')
    if not os.path.exists(database_path):
        raise FileNotFoundError(f'Database not found. Specified file path: {database_path}')
    if not os.path.exists(shp_path):
        raise FileNotFoundError(f'Shapefile not found. Specified path: {shp_path}')
    if not os.path.exists(locations_path):
        raise FileNotFoundError(f'Locations not found. Specified path: {shp_path}')

    return parser
