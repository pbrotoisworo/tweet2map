class RunConfig:
    """
    Initialize settings from the .ini file
    """

    def __init__(self, file):
        self.file = file

    def reset_errors(self):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.set('settings', 'parser_error', 'False')
        with open(self.file, 'w') as f:
            parser.write(f)

    def error(self):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.set('settings', 'parser_error', 'True')
        with open(self.file, 'w') as f:
            parser.write(f)

    def tweepy_tokens(self):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read(self.file)
        parser.sections()
        consumer_key = parser.get('tweepy', 'consumer_key')
        consumer_secret = parser.get('tweepy', 'consumer_secret')
        access_token = parser.get('tweepy', 'access_token')
        access_secret = parser.get('tweepy', 'access_secret')
        return consumer_key, consumer_secret, access_token, access_secret
