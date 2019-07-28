import re
import logging


class TweetParse:

    # Class object attributes
    # Blank

    # init
    # def __init__(self, string):
    #     self.string = string.upper()

    def __str__(self):
        return f'Tweet: {self.string}'

    def get_time(self, tweet_text):
        """
        Extract time from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        import time

        tweet_text = tweet_text.replace(';', ':')
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

    def lane(self, tweet_text):
        """
        Extract lanes occupied data from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'\d\s(LANE|LANES)')
        matches = pattern.finditer(tweet_text)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.split(' ')[0]
            print(f'Lanes Blocked: {tweet_text}')
            return tweet_text

    def get_lanes_blocked(self, tweet_text):
        """
        Extract lanes occupied data from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        tweet_text = tweet_text.upper()
        pattern = re.compile(r'\d\s(LANE|LANES)')
        matches = pattern.finditer(tweet_text)
        logging.info('get_lanes_blocked(): Raw input {}'.format(tweet_text))
        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_lanes_blocked(): RegEx Match {}'.format(tweet_text))
            tweetLanes = tweet_text.split(' ')[0]
            logging.info('get_lanes_blocked(): Cleaned output {}'.format(tweetLanes))
            return tweetLanes

    def get_inc_type(self, tweet_text):
        """
        Extract incident type from the MMDA tweet.
        tweet_text: full text of twitter post
        """

        parsed_incident_type = False

        tweet_text = tweet_text.upper()
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

    def stall(self, tweet_text):
        """
        Special case. Used to parse only if 'STALLED' in tweet
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'STALLED [A-Z0-9\-\s]+DUE')
        matches = pattern.finditer(tweet_text)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('STALLED ', '')
            tweet_text = tweet_text.replace(' DUE', '')
            tweet_text = tweet_text.rstrip(' ')
        print(f'Participants: {tweet_text}')
        return tweet_text

    def direction(self, tweet_text):

        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        matches = pattern.finditer(tweet_text)
        for match in matches:
            tweetDirection = match.group(0)
            tweetDirection = tweetDirection.replace(' ', '')
        return tweetDirection

    def rally_location(self, tweet_text):
        """
        Special case. Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r' AT [A-Z0-9\s]+MORE OR')
        matches = pattern.finditer(self.string)

        for match in matches:
            tweet_text = match.group(0)
            #print(f'DEBUG: tweet_text rallyist is {tweet_text}')
            tweet_text = tweet_text.replace(' MORE OR', '')
            tweet_text = tweet_text.replace(' AT ', '')
            tweet_text = tweet_text.replace(' NB ', ' ')
            tweet_text = tweet_text.replace(' EB ', ' ')
            tweet_text = tweet_text.replace(' SB ', ' ')
            tweet_text = tweet_text.replace(' WB ', ' ')
        print(f'Location: {tweet_text}')
        return tweet_text

    def rally_participants(self, tweet_text):
        """
        Special case. Gets participants.
        Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'MORE OR LESS \d+ PAX')
        matches = pattern.finditer(self.string.upper())
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('MORE OR LESS ', '')
            print(f'Participants: {tweet_text}')
        return tweet_text

    def strip_direction(self, tweetLocation):
        """
        Parse then remove direction text from tweet
        """
        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        matches = pattern.finditer(tweetLocation)
        for match in matches:
            tweetDirection = match.group(0)
            tweetDirection = tweetDirection.replace(' ', '')
            tweetLocation = tweetLocation.replace(' NB', '')
            tweetLocation = tweetLocation.replace(' EB', '')
            tweetLocation = tweetLocation.replace(' SB', '')
            tweetLocation = tweetLocation.replace(' WB', '')
            tweetLocation = tweetLocation.replace(' NB ', ' ')
            tweetLocation = tweetLocation.replace(' EB ', ' ')
            tweetLocation = tweetLocation.replace(' SB ', ' ')
            tweetLocation = tweetLocation.replace(' WB ', ' ')
            tweetParticipant = tweetParticipant.rstrip(' ')
        return tweetLocation

    def get_direction(self, tweet_text):

        parsed_direction = False

        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        matches = pattern.finditer(tweet_text)
        for match in matches:
            tweetDirection = match.group(0)
            tweetDirection = tweetDirection.replace(' ', '')
            parsed_direction = True

        if parsed_direction == False:
            tweetDirection = ''

        return tweetDirection

    def strip_direction(self, tweetLocation):
        """
        Parse then remove direction text from tweet
        """
        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
        matches = pattern.finditer(tweetLocation)
        for match in matches:
            tweetLocation = tweetLocation.replace(' NB', '')
            tweetLocation = tweetLocation.replace(' EB', '')
            tweetLocation = tweetLocation.replace(' SB', '')
            tweetLocation = tweetLocation.replace(' WB', '')
            tweetLocation = tweetLocation.replace(' NB ', ' ')
            tweetLocation = tweetLocation.replace(' EB ', ' ')
            tweetLocation = tweetLocation.replace(' SB ', ' ')
            tweetLocation = tweetLocation.replace(' WB ', ' ')
        return tweetLocation

    def get_location(self, tweetText, strip_direction=True):

        parsed_location = False
        pattern = re.compile(r' AT\s[a-zA-Z\Ñ\'\.\,\-0-9\/\s]+(AS OF)')
        matches = pattern.finditer(tweetText.upper())
        for match in matches:
            tweetLocation = match.group(0)
            logging.info('get_location(): RegEx Match {}'.format(tweetLocation))
            tweetLocation = tweetLocation.lstrip(' ')
            tweetLocation = tweetLocation.replace('  ', ' ')
            tweetLocation = tweetLocation.split(' INVOLVING')[0]
            tweetLocation = tweetLocation.split('AT ')[1]
            tweetLocation = tweetLocation.replace(' AT ', '')
            tweetLocation = tweetLocation.replace(' AS OF', '')
            logging.info('get_location(): Cleaned Location {}'.format(tweetLocation))

            parsed_location = True

            if strip_direction == True:
                tweetLocationStrip = self.strip_direction(tweetLocation)
                logging.info('get_location(): Stripped Direction {}'.format(tweetLocationStrip))
                return tweetLocationStrip

        if parsed_location == False:
            tweetLocation = ''
        return tweetLocation

    def get_participants(self, tweetLocation):

        tweetLocation = tweetLocation.upper()
        logging.info('get_participants(): Raw input {}'.format(tweetLocation))

        if len(tweetLocation.split(' INVOLVING')) > 1:
            tweetParticipant = tweetLocation.split(' INVOLVING')[1]
            tweetParticipant = tweetParticipant.rstrip(' ')
            tweetParticipant = tweetParticipant.lstrip(' ')
            tweetParticipant = tweetParticipant.split('AS OF')[0]
            logging.info('get_participants(): Cleaned output {}'.format(tweetParticipant))
        else:
            tweetParticipant = ''

        return tweetParticipant

    def get_date(self, tweet):

        from datetime import datetime, timedelta
        tweetDate = str(tweet.created_at)
        logging.info('get_date(): Raw input {}'.format(tweetDate))
        tweetDate = datetime.strptime(tweetDate, "%Y-%m-%d %H:%M:%S")
        tweetDate = tweetDate + timedelta(hours=8)
        tweetDate = str(tweetDate).split(' ')[0]
        logging.info('get_date(): Cleaned output {}'.format(tweetDate))

        return tweetDate

    def get_rally_location(self, tweet_text):
        """
        Special case. Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """

        parsed_rally_location = False

        tweet_text = tweet_text.upper()

        pattern = re.compile(r' AT [A-Z0-9\s]+MORE OR')
        matches = pattern.finditer(tweet_text)

        logging.info('get_rally_location(): Raw input {}'.format(tweet_text))

        for match in matches:
            tweetLocation = match.group(0)
            logging.info('get_rally_location(): RegEx Match {}'.format(tweetLocation))
            tweetLocation = tweetLocation.replace(' MORE OR', '')
            tweetLocation = tweetLocation.replace(' AT ', '')
            tweetLocation = self.strip_direction(tweetLocation)
            logging.info('get_rally_location(): Cleaned string {}'.format(tweetLocation))
            parsed_rally_location = True

        if parsed_rally_location == False:
            tweetLocation = ''
            logging.info('get_rally_location(): Empty match')

        return tweetLocation

    def get_rally_participants(self, tweet_text):
        """
        Special case. Gets participants.
        Fix parse for 'RALLYIST' type event
        tweet_text: full text of twitter post
        """
        parsed_rally_participant = False
        tweet_text = tweet_text.upper()

        pattern = re.compile(r'MORE OR LESS \d+ PAX')
        matches = pattern.finditer(tweet_text)
        logging.info('get_rally_participants(): Raw input {}'.format(tweet_text))

        for match in matches:
            tweetParticipant = match.group(0)
            logging.info('get_rally_participants(): RegEx Match {}'.format(tweetParticipant))
            tweetParticipant = tweetParticipant.replace('MORE OR LESS ', '')
            logging.info('get_rally_participants(): Cleaned output {}'.format(tweetParticipant))
            parsed_rally_participant = True

        if parsed_rally_participant == False:
            tweetParticipant = ''

        return tweetParticipant

    def get_stalled_participants(self, tweetText):
        """
        Special case. Used to parse only if 'STALLED' in tweet
        tweet_text: full text of twitter post
        """
        tweetText = tweetText.upper()
        parsed_stalled_participants = False
        logging.info('get_stalled_participants(): Raw input {}'.format(tweetText))

        pattern = re.compile(r'STALLED [A-Z0-9\-\s]+DUE')
        matches = pattern.finditer(tweetText)
        for match in matches:
            tweet_text = match.group(0)
            logging.info('get_stalled_participants(): RegEx Match {}'.format(tweet_text))
            tweet_text = tweet_text.replace('STALLED ', '')
            tweet_text = tweet_text.replace(' DUE', '')
            tweetParticipants = tweet_text.rstrip(' ')
            logging.info('get_stalled_participants(): Cleaned String {}'.format(tweetParticipants))
            parsed_stalled_participants = True

        if parsed_stalled_participants == False:
            tweetParticipants = ''
            logging.info('get_stalled_participants(): Empty Match {}'.format(tweetParticipants))

        return tweetParticipants
