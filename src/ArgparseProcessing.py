from configparser import ConfigParser
import argparse

def argparse_generate_flags(parser):
    """Function to handle CLI input"""
    
    # Define CLI inputs
    cli_args = parser.add_argument_group('Arguments')
    # cli_args.add_argument('-v', help='Verbose mode', action='store_true')
    cli_args.add_argument('-p', help='Process tweets', action='store_true')
    cli_args.add_argument('-csv_out_path', help='CSV output path for SQL database conversion')
    cli_args.add_argument('-consumer_key', help='Twitter API consumer key')
    cli_args.add_argument('-consumer_secret', help='Twitter API consumer secret')
    cli_args.add_argument('-access_token', help='Twitter API access token')
    cli_args.add_argument('-access_secret', help='Twitter API access secret')
    cli_args.add_argument('-inc_database_path', help='Incident database path')
    cli_args.add_argument('-shp_path', help='Shapefile path')
    cli_args.add_argument('-loc_database_path', help='Location database path')
    
    return parser
    
def argparse_processing(args: dict, config: str):
    """
    Process args

    :param args: [description]
    :type args: [type]
    :param config: [description]
    :type config: [type]
    """
    tweepy_params = dict()
    tweepy_params['consumer_key'] = argparse_config(arg=args['consumer_key'], section='tweepy', arg_type='consumer_key', config_path=config)
    tweepy_params['consumer_secret'] = argparse_config(arg=args['consumer_secret'], section='tweepy', arg_type='consumer_secret', config_path=config)
    tweepy_params['access_token'] = argparse_config(arg=args['access_token'], section='tweepy', arg_type='access_token', config_path=config)
    tweepy_params['access_secret'] = argparse_config(arg=args['access_secret'], section='tweepy', arg_type='access_secret', config_path=config)
    shp_path = argparse_config(arg=args['shp_path'], section='software', arg_type='shp_path', config_path=config)
    inc_database_path = argparse_config(arg=args['inc_database_path'], section='software', arg_type='database_path', config_path=config)
    loc_database_path = argparse_config(arg=args['loc_database_path'], section='software', arg_type='locations_path', config_path=config)
    
    out_dict = {
        'tweepy_params': tweepy_params,
        'shp_path': shp_path,
        'inc_database_path': inc_database_path,
        'loc_database_path': loc_database_path
    }
    
    return out_dict

def argparse_config(arg, section, arg_type, config_path):
    """Check Tweepy details and load saved credentials if empty"""

    # Create instance
    parser = ConfigParser()
    parser.read(config_path)

    if not arg:
        # No input detected. Load saved tokens.
        tweepy_param = parser.get(section, arg_type)
    else:
        # Input detected. Update config file.
        tweepy_param = arg
        parser.set(section, arg_type, arg)
        parser.write(open(config_path, 'w'))

    return tweepy_param