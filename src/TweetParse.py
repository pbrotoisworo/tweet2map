import re
import logging
from datetime import datetime, timedelta
from src.CleanString import location_string_clean


class TweetParse:
    """Input Tweepy object containing single Tweet"""
    
    # Class object attributes
    # Blank

    def __init__(self, tweepy_tweet):
        self.tweet_text = tweepy_tweet.full_text.upper()
        self.tweepy_date = tweepy_tweet.created_at

        # Extract info
        self.time = self.get_time()
        self.date = self.get_date()
        self.lanes_blocked = self.get_lanes_blocked()
        self.incident_type = self.get_inc_type()
        self.direction = self.get_direction()
        if 'RALLY' in self.tweet_text:
            self.location = self.get_rally_location()
            self.participants = self.get_rally_participants()
        else:
            self.location = self.get_location()
            self.participants = self.get_rally_participants()
        if 'STALLED' in self.tweet_text:
            self.participants = self.get_stalled_participants()
        else:
            self.participants = self.get_participants()
        self.source = 'https://twitter.com/mmda/status/' + tweepy_tweet.id_str


    def get_time(self):
        """
        Extract time from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        import time

        tweet_text = self.tweet_text.replace(';', ':')
        pattern = re.compile(r'\d+:\d\d[\s(AM|PM)]+')
        matches = pattern.finditer(tweet_text)
        logging.info('get_time(): Raw input {}'.format(tweet_text))
        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_time(): RegEx Match {}'.format(tweet_text))
            tweet_text = tweet_text.replace('.', '')

        if len(tweet_text) > 10:
            tweet_text = ''

        # Check if there is a space in the time
        # Variables for if statements
        numList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':']

        pattern = re.compile(r'[0-9]\s[(AM|PM)]')
        matches = pattern.finditer(tweet_text)
        timeCheck = ''
        for match in matches:
            timeCheck = match.group(0)
            logging.info('get_time(): TimeCheck Var {}'.format(timeCheck))

        pattern = re.compile(r'(AM|PM)')
        matches = pattern.finditer(tweet_text)
        for match in matches:
            timeDay = match.group(0)
            logging.info('get_time(): timeDay Var {}'.format(timeDay))

        if len(timeCheck) == 0 and ('AM' in tweet_text or 'PM' in tweet_text):
            # If there is no space BUT there is AM PM then
            # execute the code below to insert a space
            stringFix = [x for x in tweet_text if x in numList]
            stringFix = ''.join(stringFix)
            tweet_text = stringFix + ' ' + timeDay
            logging.info('get_time(): Cleaned Output {}'.format(tweet_text))

        return tweet_text

    def get_lanes_blocked(self):
        """
        Extract lanes occupied data from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        tweet_text = self.tweet_text
        pattern = re.compile(r'\d\s(LANE|LANES)')
        matches = pattern.finditer(tweet_text)
        logging.info('get_lanes_blocked(): Raw input {}'.format(tweet_text))
        
        tweet_lanes = ''  # To make the variable accessible outside the for loop
        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_lanes_blocked(): RegEx Match {}'.format(tweet_text))
            tweet_lanes = tweet_text.split(' ')[0]
            logging.info('get_lanes_blocked(): Cleaned output {}'.format(tweet_lanes))
        
        return tweet_lanes

    def get_inc_type(self):
        """
        Extract incident type from the MMDA tweet.
        tweet_text: full text of twitter post
        """

        parsed_incident_type = False

        tweet_text = self.tweet_text.upper()
        pattern = re.compile(r'MMDA ALERT: [A-Za-z0-9\s]+ AT ')
        matches = pattern.finditer(tweet_text)
        logging.info('get_inc_type(): Raw input {}'.format(tweet_text))

        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_inc_type(): RegEx Match {}'.format(tweet_text))
            tweet_text = tweet_text.replace('MMDA ALERT: ', '')
            tweetType = tweet_text.replace(' AT ', '')
            logging.info('get_inc_type(): Cleaned output {}'.format(tweetType))
            parsed_incident_type = True

        if parsed_incident_type == False:
            tweetType = ''
            logging.info('get_inc_type(): Empty output')

        return tweetType

    def get_direction(self):

        parsed_direction = False

        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        matches = pattern.finditer(self.tweet_text)
        for match in matches:
            tweetDirection = match.group(0)
            tweetDirection = tweetDirection.replace(' ', '')
            parsed_direction = True

        if parsed_direction == False:
            tweetDirection = ''

        return tweetDirection

    def _strip_direction(self, text):
        """
        Parse then remove direction text from tweet
        """
        tweet_location = text
        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        # matches = pattern.finditer(tweet_location)
        # for match in matches:
        tweet_location = tweet_location.replace(' NB', '')
        tweet_location = tweet_location.replace(' EB', '')
        tweet_location = tweet_location.replace(' SB', '')
        tweet_location = tweet_location.replace(' WB', '')
        tweet_location = tweet_location.replace(' NB ', ' ')
        tweet_location = tweet_location.replace(' EB ', ' ')
        tweet_location = tweet_location.replace(' SB ', ' ')
        tweet_location = tweet_location.replace(' WB ', ' ')
        return tweet_location

    def get_location(self, strip_direction=True):

        pattern = re.compile(r' AT\s[a-zA-Z\Ñ\'\.\,\-0-9\/\s]+(AS OF)')
        matches = pattern.finditer(self.tweet_text)
        tweet_location = ''
        for match in matches:
            tweet_location = match.group(0)
            logging.info('get_location(): RegEx Match {}'.format(tweet_location))
            tweet_location = tweet_location.lstrip(' ')
            tweet_location = tweet_location.replace('  ', ' ')
            tweet_location = tweet_location.split(' INVOLVING')[0]
            tweet_location = tweet_location.split('AT ')[1]
            tweet_location = tweet_location.replace(' AT ', '')
            tweet_location = tweet_location.replace(' AS OF', '')
            tweet_location = location_string_clean(tweet_location)
            logging.info('get_location(): Cleaned Location {}'.format(tweet_location))

            if strip_direction:
                tweet_location = self._strip_direction(tweet_location)
                logging.info('get_location(): Stripped Direction {}'.format(tweet_location))

        tweet_location = tweet_location.replace('Ñ', 'N')
        tweet_location = tweet_location.rstrip(' ')
        tweet_location = tweet_location.lstrip(' ')
        
        return tweet_location

    def get_participants(self):

        tweet_participant = self.tweet_text
        logging.info('get_participants(): Raw input {}'.format(tweet_participant))

        if len(tweet_participant.split(' INVOLVING')) > 1:
            tweet_participant = tweet_participant.split(' INVOLVING')[1]
            tweet_participant = tweet_participant.rstrip(' ')
            tweet_participant = tweet_participant.lstrip(' ')
            tweet_participant = tweet_participant.split('AS OF')[0]
            logging.info('get_participants(): Cleaned output {}'.format(tweet_participant))
        else:
            tweet_participant = ''

        return tweet_participant

    def get_date(self):

        tweetDate = str(self.tweepy_date)
        logging.info('get_date(): Raw input {}'.format(tweetDate))
        tweetDate = datetime.strptime(tweetDate, "%Y-%m-%d %H:%M:%S")
        tweetDate = tweetDate + timedelta(hours=8)
        tweetDate = str(tweetDate).split(' ')[0]
        logging.info('get_date(): Cleaned output {}'.format(tweetDate))

        return tweetDate

    def get_rally_location(self):
        """
        Special case. Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """

        parsed_rally_location = False

        tweet_text = self.tweet_text

        pattern = re.compile(r' AT [A-Z0-9\s]+MORE OR')
        matches = pattern.finditer(tweet_text)

        logging.info('get_rally_location(): Raw input {}'.format(tweet_text))

        for match in matches:
            tweetLocation = match.group(0)
            logging.info('get_rally_location(): RegEx Match {}'.format(tweetLocation))
            tweetLocation = tweetLocation.replace(' MORE OR', '')
            tweetLocation = tweetLocation.replace(' AT ', '')
            tweetLocation = self._strip_direction(tweetLocation)
            logging.info('get_rally_location(): Cleaned string {}'.format(tweetLocation))
            parsed_rally_location = True

        if parsed_rally_location == False:
            tweetLocation = ''
            logging.info('get_rally_location(): Empty match')

        return tweetLocation

    def get_rally_participants(self):
        """
        Special case. Gets participants.
        Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """
        parsed_rally_participant = False
        tweet_text = self.tweet_text

        pattern = re.compile(r'MORE OR LESS \d+ PAX')
        matches = pattern.finditer(tweet_text)
        logging.info('get_rally_participants(): Raw input {}'.format(tweet_text))

        for match in matches:
            tweet_participant = match.group(0)
            logging.info('get_rally_participants(): RegEx Match {}'.format(tweet_participant))
            tweet_participant = tweet_participant.replace('MORE OR LESS ', '')
            logging.info('get_rally_participants(): Cleaned output {}'.format(tweet_participant))
            parsed_rally_participant = True

        if parsed_rally_participant == False:
            tweet_participant = ''

        return tweet_participant

    def get_stalled_participants(self):
        """
        Special case. Used to parse only if 'STALLED' in tweet
        tweet_text: full text of twitter post
        """
        tweetText = self.tweet_text
        parsed_stalled_participants = False
        logging.info('get_stalled_participants(): Raw input {}'.format(tweetText))

        pattern = re.compile(r'STALLED [A-Z0-9\-\s]+DUE')
        matches = pattern.finditer(tweetText)
        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_stalled_participants(): RegEx Match {}'.format(tweet_text))
            tweet_text = tweet_text.replace('STALLED ', '')
            tweet_text = tweet_text.replace(' DUE', '')
            tweet_participants = tweet_text.rstrip(' ')
            logging.info('get_stalled_participants(): Cleaned String {}'.format(tweet_participants))
            parsed_stalled_participants = True

        if parsed_stalled_participants == False:
            tweet_participants = ''
            logging.info('get_stalled_participants(): Empty Match {}'.format(tweet_participants))

        return tweet_participants
