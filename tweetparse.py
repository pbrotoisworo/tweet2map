import re


class tweetParse:

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
        pattern = re.compile(r'\d+\D\d\d[\s(AM|PM)]')
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('.', '')
            tweet_text = tweet_text.replace(';', ':')
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
        matches = pattern.finditer(self.string)
        for match in matches:
            tweet_text = match.group(0)
            tweet_text = tweet_text.replace('MORE OR LESS ', '')
            print(f'Participants: {tweet_text}')
        return tweet_text

#     def strip_direction(self, tweet_text):
#         """
#         Remove direction text from tweet
#         """
#         pattern = re.compile(r'( SB | NB | WB | EB )')
#         matches = pattern.finditer(self.string)
#         for match in matches:
#             tweet_text = match.group(0)
#             tweet_text = tweet_text.replace(' ', '')
#             tweet_text = tweet_text.replace(' NB', '')
#             tweet_text = tweet_text.replace(' EB', '')
#             tweet_text = tweet_text.replace(' SB', '')
#             tweet_text = tweet_text.replace(' WB', '')
        return tweet_text
