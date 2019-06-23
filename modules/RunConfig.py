# initialization scripts for Tweet2Map
from configparser import ConfigParser
import tweepy


class RunConfig:
    """
    Class to run different operations on the config file
    """

    def __init__(self, file):
        self.file = file

    def reset_errors(self):
        """
        Reset the parser_error status to FALSE.
        At the end of the Tweet2Map script there is a check
        to see if an error was raised. This resets the status
        so the script can continue even if there was no error.
        """
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.set('settings', 'parser_error', 'False')
        parser.set('settings', 'arcpy_run', 'True')
        with open(self.file, 'w') as f:
            parser.write(f)

    def arcpy_prevent_parser_error(self):
        """
        Change parser_error to True. This will prevent the ArcPy
        script from running when a Tweet2Map error occurs.
        """
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.set('settings', 'parser_error', 'True')
        with open(self.file, 'w') as f:
            parser.write(f)

    def arcpy_prevent_empty_input(self):
        """
        If there is empty input from the tweet
        then prevent the arcpy script from executing
        """
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.set('settings', 'arcpy_run', 'False')
        with open(self.file, 'w') as f:
            parser.write(f)

    def tweepy_tokens(self):
        """
        Import Twitter API tokens from the config file
        """
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.sections()
        consumer_key = parser.get('tweepy', 'consumer_key')
        consumer_secret = parser.get('tweepy', 'consumer_secret')
        access_token = parser.get('tweepy', 'access_token')
        access_secret = parser.get('tweepy', 'access_secret')
        return consumer_key, consumer_secret, access_token, access_secret

    def dir_databases(self):
        """
        Directory for databases
        """
        parser = ConfigParser()
        parser.read(self.file)
        parser.sections()
        database_main = parser.get('database', 'main')
        database_copy_gis = parser.get('database', 'gis')
        database_no_null = parser.get('database', 'main_no_null')

        return database_main, database_copy_gis, database_no_null
