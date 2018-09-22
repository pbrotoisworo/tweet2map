# Encoding: utf-8

import tweepy
import re
import time
import csv
import pandas as pd
from function_list import location_string_clean
from tweetparse import tweetParse

print('MMDA Tweet2Map Version 0.7')
print('Panji Brotoisworo')
print('Contact: panji.p.broto@gmail.com')
print('Website: https://panjib.wixsite.com/blog/mmdatweet2map')
print(f'\nStarting application...\n')

file_location_strings = {}
ListDirection = ['NB', 'SB', 'EB', 'WB']
ListDirectionCheck = [' NB ', ' SB ', ' EB ', ' WB ']
lst_tweets = []
lst_duplicate_check = []
UserBreak = False
file_locations = 'dictionary_database.txt'
file_dataset = 'data_mmda_traffic_alerts.csv'

# Load database of string locations or create one if it doesn't exist
try:
    f_DBLocationStrings = open(file_locations, 'r')
    for line in f_DBLocationStrings:
        x = line.split("/")
        x[1] = x[1].replace('\n', '')
        x[1] = x[1].replace(' ', '')
        file_location_strings[x[0]] = x[1]
    f_DBLocationStrings.close()
    print('Location database loaded.')
except FileNotFoundError:
    print('Database not detected. Creating new txt file')
    # Create file for read and write
    f_DBLocationStrings = open(file_locations, 'x+')

# Load last set of tweets to check for duplicates
try:
    with open(file_dataset, 'r', newline='') as CsvFile:
        reader = csv.reader(CsvFile)

        for idx, row in enumerate(reversed(list(CsvFile))):
            DataRow = row
            DataRow = DataRow.replace('\r\n', '')
            lst_duplicate_check.append(DataRow.split(',')[-1])
            if idx == 200:
                print('Duplicate check initialized')
                break

except FileNotFoundError:
    print('CSV file not detected. Creating new CSV file')
    with open(file_dataset, 'x', newline='') as CsvFile:
        # reader = csv.reader(CsvFile)
        for idx, row in enumerate(reversed(list(CsvFile))):
            DataRow = row
            DataRow = DataRow.replace('\r\n', '')
            lst_duplicate_check.append(DataRow.split(',')[-1])
            if idx == 200:
                break

print(f'Location Database loaded! {len(file_location_strings)} entries.\n')
print(f'Tweet Data:\n')

# Tweepy Settings
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
tweets = api.user_timeline(screen_name="mmda", count=200, include_rts=False)

# Code that will analyze each tweet
for info in reversed(tweets):

    # Declared variables that need to be reset every loop
    twt_type = ''
    twt_participant = ''
    twt_location = ''
    twt_direction = ''
    twt_time = ''
    twt_date = ''
    twt_lane = ''
    twt_id = ''
    twt_text = ''
    twt_type = ''
    twt_latitude = ''
    twt_longitude = ''
    check_location_add = False
    duplicate_check = False

    # Only look at their MMDA ALERT tweets
    if 'MMDA ALERT' in info.text.upper():

        # Get post ID and check if it is a duplicate tweet
        twt_id = 'https://twitter.com/mmda/status/' + str(info.id)
        if twt_id in lst_duplicate_check:
            print('Duplicate Data! Skipping to next tweet.')
            duplicate_check = True
            continue
        else:
            # Get date and text
            twt_date = info.created_at
            twt_date = twt_date.strftime("%m-%d-%Y")
            twt_text = info.text
            info = info.text.upper()
            lst_tweets.append(info)

            print('-------------------------------')
            print(f'Tweet: {info}')
            print(f'Date: {twt_date}')
            print(f'URL: {twt_id}')

            # Call on the TweetParse class
            twt = tweetParse(twt_text)
            twt_time = twt.time(twt_text)
            twt_type = twt.inc_type(twt_text)
            twt_lane = twt.lane(twt_text)

            # Get location, participants, and direction
            pattern = re.compile(r' AT\s[a-zA-Z\Ñ\'\.\,\-0-9\/\s]+(AS OF)')
            matches = pattern.finditer(info)
            for match in matches:
                twt_location = match.group(0)
                # Location String Cleaning
                twt_location = location_string_clean(twt_location)

                # ELLIPTICAL ROAD in QC can confuse parser sometimes
                if 'ELLIPTICAL' not in twt_location:
                    # Get direction then remove direction
                    # twt_location = twt.strip_direction(twt_text)
                    pattern = re.compile(r'( SB | NB | WB | EB )')
                    matches = pattern.finditer(info)
                    for match in matches:
                        twt_direction = match.group(0)
                        twt_direction = twt_direction.replace(' ', '')
                        twt_location = twt_location.replace(' NB', '')
                        twt_location = twt_location.replace(' EB', '')
                        twt_location = twt_location.replace(' SB', '')
                        twt_location = twt_location.replace(' WB', '')
                    print(f'Direction: {twt_direction}')

                    # Get participants
                    if len(twt_location.split(' INVOLVING')) > 1:
                        twt_participant = twt_location.split(' INVOLVING')[1]
                        twt_participant = twt_participant.rstrip(' ')
                        twt_participant = twt_participant.lstrip(' ')
                        if len(twt_participant) > 0:
                            print(f'Participants: {twt_participant}')

                    twt_location = twt_location.split('INVOLVING')[0].strip(' ')
                    print(f'Location: {twt_location}')

                if 'ELLIPTICAL' in twt_location:

                    if 'ELLIPTICAL' and 'NORTH' in twt_location:
                        twt_location = 'ELLIPTICAL ROAD NORTH AVE.'
                    elif 'ELLIPTICAL' and 'QUEZON' in twt_location:
                        twt_location = 'ELLIPTICAL ROAD QUEZON AVE.'
                    elif 'ELLIPTICAL' and 'VISAYAS' in twt_location:
                        twt_location = 'ELLIPTICAL ROAD VISAYAS AVE.'
                    elif 'ELLIPTICAL' and 'EAST AVE' in twt_location:
                        twt_location = 'ELLIPTICAL ROAD EAST AVE.'
                    elif 'ELLIPTICAL' and ' DAR ' in twt_location:
                        twt_location = 'ELLIPTICAL ROAD DAR'
                    else:
                        twt_location = input('Enter elliptical road location:')
                    # twt_participant = input('TEMPORARY. Enter participants:')
                    # Get participants
                    if len(twt_location.split(' INVOLVING')) > 1:
                        twt_participant = twt_location.split(' INVOLVING')[1]
                        twt_participant = twt_participant.rstrip(' ')
                        twt_participant = twt_participant.lstrip(' ')
                        print(f'Participants: {twt_participant}')
                    # print(f'DEBUG: twt_location is {twt_location}')
                    print(f'Participants: {twt_participant}')
                    print(f'Location: {twt_location}')
                    print(f'Direction: {twt_direction}')

            # Special case. Get participants
            if 'STALLED' in info:
                twt_participant = twt.stall(twt_text)

            # Special case. Get location and participants
            if 'RALLYIST' in info:
                twt_type = 'RALLYIST'
                # Get location and participants
                twt_location = twt.rally_location(twt_text)
                twt_participant = twt.rally_participants(twt_text)

            # Check location with database
            try:
                #print(f'DEBUG: twt_location is {twt_location}')
                twt_latitude = file_location_strings[twt_location].split(',')[0]
                twt_longitude = file_location_strings[twt_location].split(',')[1]
                print(f'Latitude: {twt_latitude}')
                print(f'Longitude: {twt_longitude}')
                check_location_add = True

            except KeyError:
                # User input to check if location string is correct
                # if it is correct,, type YES to add it, if not, type NO to manual fix

                print(f'\nNew location detected! {twt_location} is not recognized.')
                print(f'\nChoose number from list:')
                print('1 - Add new location and new coordinates')
                print(f'2 - Add new location based on existing coordinates\n')
                # print(f'3 - Rename location then use existing coordinates\n')
                #print(f'3 - Auto recommend (BETA)')

                user_loc_choice = input('Enter number to proceed:')

                # Declare variable to control while loop
                user_loc_choiceCheck = False

                while user_loc_choiceCheck == False:

                    if user_loc_choice == 'BREAK':
                        UserBreak = True
                        break

                    elif user_loc_choice == '1':
                        print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
                        user_input_coord = input('Enter coordinates:')
                        user_input_coord = user_input_coord.replace(' ', '')
                        twt_latitude = user_input_coord.split(',')[0]
                        twt_longitude = user_input_coord.split(',')[1]
#                           print(f'DEBUG: user_input_coord is {user_input_coord}')
#                           print(f'DEBUG: twt_latitude is {twt_latitude}')
#                           print(f'DEBUG: twt_latitude is {twt_longitude}')
                        print(f'\nData to be added:')
                        print(
                            f'Location: {twt_location}\nLatitude: {twt_latitude}\nLongitude: {twt_longitude}')
                        user_append_locdatabase = input('Confirm information is correct? (Y/N)')

                        # Append to loc_ database dictionary
                        if user_append_locdatabase == 'Y':
                            file_location_strings[twt_location] = twt_latitude + ',' + twt_longitude
                            user_loc_choiceCheck = True
                            check_location_add = True
                        elif user_append_locdatabase == 'N':
                            continue
                        elif user_append_locdatabase == 'BREAK':
                            break

                    elif user_loc_choice == '2':
                        user_search = input('Search database for existing location: ').upper()
                        print(f'Search results with {user_search}')

                        # Get match to dictionary location
                        for idx, loc in enumerate(file_location_strings):
                            if user_search in loc:
                                print(idx, loc)
                                #UserSearchStringMatch = loc

                        UserSearchCoordMatch = input('Choose index number: ')

                        for idx, item in enumerate(file_location_strings.items()):
                            if idx == int(UserSearchCoordMatch):
                                print(idx, item)
                                #print(f'item is {type(item)}')
                                twt_latitude = item[1].split(',')[0]
                                twt_longitude = item[1].split(',')[1]
                                #print(f'DEBUG: twt_latitude is {twt_latitude}')
                                #print(f'DEBUG: twt_latitude is {twt_longitude}')

                        print(
                            f'Data to be added:\nLocation: {twt_location}\nLatitude: {twt_latitude}\nLongitude: {twt_longitude}')
                        user_append_locdatabase = input('Confirm information is correct? (Y/N) ')

                        # APPEND NEW INFO BASED ON EXISTING COORDS
                        if user_append_locdatabase == 'Y':
                            UserSearchCoordMatch = twt_latitude + ',' + twt_longitude
                            file_location_strings[twt_location] = UserSearchCoordMatch
                            check_location_add = True
                            user_loc_choiceCheck = True
                        elif user_append_locdatabase == 'N':
                            pass
                    # elif user_loc_choice == '3':
                    #    pass

                    else:
                        print('Invalid input!')
                        print('Enter details again.')

                if twt_location == 'BREAK':
                    UserBreak = True
                    break

            if UserBreak == True:
                break

            if check_location_add == False:
                twt_latitude = file_location_strings[twt_location].split(',')[0]
                twt_longitude = file_location_strings[twt_location].split(',')[1]
                print(f'Latitude: {twt_latitude}')
                print(f'Longitude: {twt_longitude}')

    if UserBreak == True:
        break

    if duplicate_check == False:

        WriteCombinedDict = {'Date': twt_date, 'Time': twt_time, 'Location': twt_location, 'Latitude': twt_latitude,
                             'Longitude': twt_longitude, 'Direction': twt_direction, 'Type': twt_type,
                             'Lanes Blocked': twt_lane, 'Involved': twt_participant, 'Tweet': twt_text, 'Source': twt_id}

        keys = WriteCombinedDict.keys()

        if twt_id in lst_duplicate_check:
            print('Duplicate data! Skipping to next tweet.')
            continue

        elif twt_id not in lst_duplicate_check:

            with open(file_dataset, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                try:
                    header_check = next(reader)
                except StopIteration:
                    header_check = []

                if header_check != []:
                    with open(file_dataset, 'a', newline='', encoding='utf-8') as CsvFile:
                        dict_writer = csv.DictWriter(CsvFile, keys)
                        dict_writer.writerow(WriteCombinedDict)
                else:
                    # Then this is just an empty CSV file so we use write
                    print(f'\nNo data in the CSV! Adding header to CSV file')
                    with open(file_dataset, 'w', newline='', encoding='utf-8') as CsvFile:
                        dict_writer = csv.DictWriter(CsvFile, keys)
                        dict_writer.writeheader()
                        dict_writer.writerow(WriteCombinedDict)


print(f'\nUpdating location database...')
f_DBLocationStrings = open(file_locations, 'w')
for x, y in file_location_strings.items():
    #     print(x,y)
    #     print(type(x),type(y))
    f_DBLocationStrings.writelines(x + '/' + y + '\n')
f_DBLocationStrings.close()

# Drop empty rows generated
df = pd.read_csv(file_dataset)
df.dropna(axis=0, subset=['Source'], inplace=True)
# df.reset_index()
df.to_csv(file_dataset, index=False)

print('Tweet analysis finished.')

program_exit = input('Press ENTER to finish ')
