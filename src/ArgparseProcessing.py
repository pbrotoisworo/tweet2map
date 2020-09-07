from configparser import ConfigParser

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