# Encoding: utf-8

print('MMDA Tweet2Map Version 0.8')
print('Panji Brotoisworo')
print('Contact: panji.p.broto@gmail.com')
print('Website: https://panjib.wixsite.com/blog/mmdatweet2map')
print(f'\nStarting application...\n')

print('Initializing Libraries...')
import tweepy
import re
import time
import csv
from function_list import location_string_clean
import time
import numpy as np
from shutil import copy
from tweetparse import tweetParse
import pandas as pd

# Initial connection check
userConnection = False
while userConnection == False:
    try:
        # Tweepy Settings
        consumer_key = 'YRoCykGzWaoZJ5ehnPxQ0Hubc'
        consumer_secret = 'XwTweV1RdrMyEqDFfuKX5eS8COSEOahNbK87wJJX4YFoLNF8Vg'
        access_token = '225641768-97zmIlo1bOeVSE3nSWvWA4bLuMswbu20mD1wcPkk'
        access_secret = 'YmBBHQ6vSmf4GeiX7GKx2Tx2a9E7hv7xAxTtWV6mODOuN'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name="mmda", count=200, include_rts=False)
        # If it can connect, then get out of the while loop
        userConnection = True
    except:
        print('Connection attempt failed!')
        print('Retrying in 60 seconds')
        time.sleep(60)

file_location_strings = {}
ListDirection = ['NB', 'SB', 'EB', 'WB']
ListDirectionCheck = [' NB ', ' SB ', ' EB ', ' WB ']
lst_tweets = []
lst_duplicate_check = []
UserBreak = False
userClose = False
tweetCounter = 0
file_locations = 'dictionary_database.txt'
file_dataset = 'data_mmda_traffic_alerts.csv'
gis_dataset = r'C:\GIS\Data Files\Work Files\MMDA Tweet2Map\input\data_mmda_traffic_alerts.csv'

# Load database of string locations or create one if it doesn't exist
try:
    f_DBLocationStrings = open(file_locations, 'r')
    for line in f_DBLocationStrings:
        x = line.split("/")
        x[1] = x[1].replace('\n', '')
        x[1] = x[1].replace(' ', '')
        file_location_strings[x[0]] = x[1]
    f_DBLocationStrings.close()
    #print('Location database loaded.')
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
                #print('Duplicate check initialized')
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

# Main loop that processes each tweet
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
    location_add_check = False
    duplicate_check = False
    alert_check = False
    UserBreak = False

    # Only look at their MMDA ALERT tweets
    if 'MMDA ALERT' in info.text.upper():

        alert_check = True

        # Check if Tweet is duplicate from database
        twt_id = 'https://twitter.com/mmda/status/' + str(info.id)
        if twt_id in lst_duplicate_check:
            print('Duplicate Data! Skipping to next tweet.')
            duplicate_check = True
            continue
        else:
            tweetCounter += 1
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
                    # print(f'DEBUG: CHECKPOINT1-{twt_location}')

                    # Get participants
                    if len(twt_location.split(' INVOLVING')) > 1:
                        # print(f'DEBUG: CHECKPOINT1.1-{twt_location}')
                        twt_participant = twt_location.split(' INVOLVING')[1]
                        twt_participant = twt_participant.rstrip(' ')
                        twt_participant = twt_participant.lstrip(' ')
                        if len(twt_participant) > 0:
                            print(f'Participants: {twt_participant}')

                    twt_location = twt_location.split('INVOLVING')[0].strip(' ')
                    print(f'Location: {twt_location}')

                    # Consider deletion
                    # Direction given. NO INVOLVED
                    if len(twt_location.split(' INVOLVING')) < 1:
                        print(f'DEBUG: CHECKPOINT2.1-{twt_location}')
                        twt_participant = twt_location.split(' AS OF ')[0]
                        twt_participant = twt_participant.rstrip(' ')
                        twt_participant = twt_participant.lstrip(' ')
                        if len(twt_participant) > 0:
                            print(f'Participants: {twt_participant}')

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
                # twt_location = twt.rally_location(twt_text)
                twt_participant = twt.rally_participants(twt_text)

    # Check for UserBreak
    if twt_location == 'BREAK':
        UserBreak = True
        break

    if alert_check == True:
        # Check location with database
        # Declare variable to control while loop
        user_loc_choice_check = False
        user_error = False
        while user_loc_choice_check == False:
            try:
                twt_latitude = file_location_strings[twt_location].split(',')[0]
                twt_longitude = file_location_strings[twt_location].split(',')[1]
                print(f'Latitude: {twt_latitude}')
                print(f'Longitude: {twt_longitude}')
                # Location is already added. Set check states to true
                location_add_check = True
                user_loc_choice_check = True

            except KeyError:
                # User input to check if location string is correct
                # if it is correct, type YES to add it, if not, type NO to manual fix

                print(f'\nNew location detected! {twt_location} is not recognized.')
                print(f'\nChoose number from list:')
                print('1 - Add new location and new coordinates')
                print(f'2 - Add new location based on existing coordinates\n')

                user_loc_choice = input('Enter number to proceed:')

                # While loop to check location
                # The check variable is if the user's location is valid
                # If valid, break out of while loop
                while location_add_check == False and user_loc_choice_check == False:

                    user_reset = False

                    if user_loc_choice == 'BREAK':
                        UserBreak = True
                        break

                    elif user_loc_choice == '1':
                        print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
                        user_input_coord = input('Enter coordinates:')
                        user_input_coord = user_input_coord.replace(' ', '')
                        twt_latitude = user_input_coord.split(',')[0]
                        twt_longitude = user_input_coord.split(',')[1]
                        # print(f'DEBUG: user_input_coord is {user_input_coord}')
                        # print(f'DEBUG: twt_latitude is {twt_latitude}')
                        # print(f'DEBUG: twt_latitude is {twt_longitude}')
                        print(f'\nData to be added:')
                        print(
                            f'Location: {twt_location}\nLatitude: {twt_latitude}\nLongitude: {twt_longitude}')
                        user_append_locdatabase = input(
                            'Confirm information is correct? (Y/N)').upper()

                        # Y - Append to loc_database dictionary
                        if user_append_locdatabase == 'Y':
                            file_location_strings[twt_location] = twt_latitude + \
                                ',' + twt_longitude
                            user_loc_choice_check = True
                            location_add_check = True

                        elif user_append_locdatabase == 'N':
                            break

                        elif user_append_locdatabase == 'BREAK':
                            UserBreak = True
                            break

                    elif user_loc_choice == '2':
                        user_search = input('Search database for existing location: ').upper()
                        if user_search == 'BREAK':
                            UserBreak = True
                            break

                        print(f'Search results with {user_search}')

                        # Get match to dictionary location
                        for idx, loc in enumerate(file_location_strings):
                            if user_search in loc:
                                print(idx, loc)
                                # UserSearchStringMatch = loc
                        print('Type "RESET" to search again.')
                        UserSearchCoordMatch = input('Choose index number: ')
                        if UserSearchCoordMatch == 'BREAK':
                            UserBreak = True
                            break
                        if UserSearchCoordMatch == 'RESET':
                            UserSearchCoordMatch = ''
                            user_search = ''
                            user_input_coord = ''
                            twt_latitude = ''
                            twt_longitude = ''
                            user_loc_choice = ''
                            user_append_locdatabase = ''
                            user_reset = True
                            print('Enter details again.')
                            break

                        for idx, item in enumerate(file_location_strings.items()):
                            if idx == int(UserSearchCoordMatch):
                                print(idx, item)
                                twt_latitude = item[1].split(',')[0]
                                twt_longitude = item[1].split(',')[1]

                        print(
                            f'Data to be added:\nLocation: {twt_location}\nLatitude: {twt_latitude}\nLongitude: {twt_longitude}')
                        user_append_locdatabase = input(
                            'Confirm information is correct? (Y/N) ').upper()

                        # APPEND NEW INFO BASED ON EXISTING COORDS
                        if user_append_locdatabase == 'Y':
                            UserSearchCoordMatch = twt_latitude + ',' + twt_longitude
                            file_location_strings[twt_location] = UserSearchCoordMatch
                            location_add_check = True
                            user_loc_choice_check = True
                        elif user_append_locdatabase == 'N':
                            UserSearchCoordMatch = ''
                            user_search = ''
                            user_input_coord = ''
                            twt_latitude = ''
                            twt_longitude = ''
                            user_loc_choice = ''
                            user_append_locdatabase = ''
                            user_reset = True
                            print('Enter details again.')
                            break

                    else:
                        # Break out of the current while loop
                        # to start process again
                        UserSearchCoordMatch = ''
                        user_search = ''
                        user_input_coord = ''
                        twt_latitude = ''
                        twt_longitude = ''
                        user_loc_choice = ''
                        user_append_locdatabase = ''
                        user_reset = True
                        print('Enter details again.')

                        if user_append_locdatabase == 'BREAK':
                            UserBreak = True
                            break

                        if twt_location == 'BREAK':
                            UserBreak = True
                            break
                    # EXIT OUT OF TRY LOOP HERE
                    if user_reset == True:
                        break

                if UserBreak == True:
                    break

                if location_add_check == False and user_reset == False:
                    twt_latitude = file_location_strings[twt_location].split(',')[0]
                    twt_longitude = file_location_strings[twt_location].split(',')[1]
                    print(f'Latitude: {twt_latitude}')
                    print(f'Longitude: {twt_longitude}')
                    user_loc_choice_check = True

            if UserBreak == True:
                break

    if UserBreak == True:
        break

    # If it is not a duplicate then write to CSV
    if duplicate_check == False:

        WriteCombinedDict = {'Date': twt_date, 'Time': twt_time, 'Location': twt_location, 'Latitude': twt_latitude,
                             'Longitude': twt_longitude, 'Direction': twt_direction, 'Type': twt_type,
                             'Lanes Blocked': twt_lane, 'Involved': twt_participant, 'Tweet': twt_text,
                             'Source': twt_id}

        keys = WriteCombinedDict.keys()

        # if twt_id in lst_duplicate_check:
        #     print('Duplicate data! Skipping to next tweet.')
        #     continue

        if twt_id not in lst_duplicate_check:

            with open(file_dataset, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                try:
                    header_check = next(reader)
                except StopIteration:
                    header_check = []

                if header_check != []:
                    # Update version in main script folder
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

if UserBreak == True:
    print('User terminated script.')

print(f'\nUpdating location database...')
f_DBLocationStrings = open(file_locations, 'w')
for x, y in file_location_strings.items():
    f_DBLocationStrings.writelines(x + '/' + y + '\n')
f_DBLocationStrings.close()

# Drop empty rows generated
# Clean data for ArcGIS
df_1 = pd.read_csv(file_dataset)
# df_1['Latitude'].replace(' ', np.nan, inplace=True)
# df_1['Longitude'].replace(' ', '', inplace=True)

df_1['Longitude'] = df_1['Longitude'].astype(str)
df_1['Longitude'] = df_1['Longitude'].str.rstrip(' ')
df_1['Longitude'] = df_1['Longitude'].str.replace('\t', '')
df_1['Longitude'] = df_1['Longitude'].str.replace('\n', '')
df_1.replace('None', np.nan, inplace=True)
df_1.dropna(axis=0, subset=['Source'], inplace=True)
# df_1['Longitude'] = df_1['Longitude'].astype(float)
df_1.to_csv(file_dataset, index=False)

# Update dataset in GIS workspace
copy(file_dataset, gis_dataset)

print(f'Twitter analysis finished.')
print(f'Analyzed {tweetCounter} new tweets')
print(f'Executing ArcPy script... This may take a few minutes depending on your computer\n')

# program_exit = input('Press ENTER to finish ')
