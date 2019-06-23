import re


class TweetParse:

    # Class object attributes
    # Blank

    # init
    def __init__(self, string):
        self.string = string.upper()

    def __str__(self):
        return f'Tweet: {self.string}'

    def time(self, tweet_text):
        """
        Extract time from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        import time

        tweet_text = tweet_text.replace(';', ':')
        pattern = re.compile(r'\d+:\d\d[\s(AM|PM)]+')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('.', '')

        if len(tweet_text) > 10:
            tweet_text = ''

        # Check if there is a space in the time
        # Variables for if statements
        numList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':']

        pattern = re.compile(r'[0-9]\s[(AM|PM)]')
        matches = pattern.finditer(self.string)
        timeCheck = ''
        for match in matches:
            timeCheck = match.group(0)

        pattern = re.compile(r'(AM|PM)')
        matches = pattern.finditer(self.string)
        for match in matches:
            timeDay = match.group(0)

        if len(timeCheck) == 0 and ('AM' in tweet_text or 'PM' in tweet_text):
            # If there is no space BUT there is AM PM then
            # execute the code below to insert a space
            stringFix = [x for x in tweet_text if x in numList]
            stringFix = ''.join(stringFix)
            tweet_text = stringFix + ' ' + timeDay

            time.sleep(1)
            print(f'DEBUG: timeCheck is {timeCheck}')
            print(f'DEBUG: checkList is {timeDay}')
            print('DEBUG: TIME FIXED')

        print(f'Time: {tweet_text}')
        return tweet_text

    def lane(self, tweet_text):
        """
        Extract lanes occupied data from the MMDA tweet. Output is string.
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'\d\s(LANE|LANES)')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.split(' ')[0]
            if tweet_text == '':
                tweet_text = input('Manual correction needed! Input lanes blocked: ')
                if tweet_text == 'BREAK':
                    break
            print(f'Lanes Blocked: {tweet_text}')
            return tweet_text

    def inc_type(self, tweet_text):
        """
        Extract incident type from the MMDA tweet.
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'MMDA ALERT: [A-Za-z0-9\s]+ AT ')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            # print(f'DEBUG: CLASS inc_type {tweet_text}')
            tweet_text = tweet_text.replace('MMDA ALERT: ', '')
            tweet_text = tweet_text.replace(' AT ', '')
        print(f'Type: {tweet_text}')
        return tweet_text

    def stall(self, tweet_text):
        """
        Special case. Used to parse only if 'STALLED' in tweet
        tweet_text: full text of twitter post
        """
        pattern = re.compile(r'STALLED [A-Z0-9\-\s]+DUE')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('STALLED ', '')
            tweet_text = tweet_text.replace(' DUE', '')
            tweet_text = tweet_text.rstrip(' ')
        print(f'Participants: {tweet_text}')
        return tweet_text

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

    def strip_direction(self, tweet_text):
        """
        Remove direction text from tweet
        """
        pattern = re.compile(r'( SB| NB| WB| EB)')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            # tweet_text = tweet_text.replace(' ', '')
            tweet_text = tweet_text.replace(' NB', '')
            tweet_text = tweet_text.replace(' EB', '')
            tweet_text = tweet_text.replace(' SB', '')
            tweet_text = tweet_text.replace(' WB', '')
        return tweet_text
