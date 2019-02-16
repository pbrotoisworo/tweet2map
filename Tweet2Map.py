# Encoding: utf-8

print('MMDA Tweet2Map Version 0.9')
print('Panji P. Brotoisworo')
print('Contact: panji.p.broto@gmail.com')
print('Website: https://panjib.wixsite.com/blog/mmdatweet2map')
print(f'\nInitializing Libraries...')

import tweepy
import re
import time
import csv
from modules.function_list import location_string_clean
from modules.TweetParse import TweetParse
from modules.RunConfig import RunConfig
import time
import numpy as np
from shutil import copy
import pandas as pd
from configparser import ConfigParser
from datetime import datetime, timedelta
import traceback

# Create RunConfig object for settings
config = RunConfig('config.ini')
config.reset_errors()

# Initial connection check
print('Connecting to API...')
userConnection = False
while userConnection == False:
    try:
        # Tweepy Settings
        consumer_key = config.tweepy_tokens()[0]
        consumer_secret = config.tweepy_tokens()[1]
        access_token = config.tweepy_tokens()[2]
        access_secret = config.tweepy_tokens()[3]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name="mmda", count=200, include_rts=False)
        # If it can connect, then get out of the while loop
        userConnection = True
    except:
        print('Connection attempt failed!')
        print('Retrying in 15 seconds')
        time.sleep(15)

databaseLocationsDictionary = {}
#ListDirection = ['NB', 'SB', 'EB', 'WB']
#ListDirectionCheck = [' NB ', ' SB ', ' EB ', ' WB ']
lstTweets = []
lstDuplicateCheck = []
userBreak = False
userClose = False
tweetCounter = 0
databaseLocations = r'modules\dictionary_database.txt'
databaseMain = 'data_mmda_traffic_alerts.csv'
databaseGIS = r'C:\GIS\Data Files\Work Files\MMDA Tweet2Map\input\data_mmda_traffic_alerts.csv'

# Load database of string locations or create one if it doesn't exist
print(f'Loading database...\n')
try:
    databaseLocationsFile = open(databaseLocations, 'r')
    for line in databaseLocationsFile:
        x = line.split("/")
        x[1] = x[1].replace('\n', '')
        x[1] = x[1].replace(' ', '')
        databaseLocationsDictionary[x[0]] = x[1]
    databaseLocationsFile.close()
    #print('Location database loaded.')

except:
    traceback.print_exc()
    config.arcpy_prevent_parser_error()
    exit()
# except FileNotFoundError:
#     print('Database not detected. Creating new txt file')
#     # Create file for read and write
#     databaseLocationsFile = open(databaseLocations, 'x+')

# Load last set of tweets to check for duplicates
try:
    with open(databaseMain, 'r', newline='') as CsvFile:
        reader = csv.reader(CsvFile)

        for idx, row in enumerate(reversed(list(CsvFile))):
            dataRow = row
            dataRow = dataRow.replace('\r\n', '')
            lstDuplicateCheck.append(dataRow.split(',')[-1])
            if idx == 200:
                #print('Duplicate check initialized')
                break

except FileNotFoundError:
    print('CSV file not detected. Creating new CSV file')
    with open(databaseMain, 'x', newline='') as CsvFile:
        # reader = csv.reader(CsvFile)
        for idx, row in enumerate(reversed(list(CsvFile))):
            dataRow = row
            dataRow = dataRow.replace('\r\n', '')
            lstDuplicateCheck.append(dataRow.split(',')[-1])
            if idx == 200:
                break

print(f'Location Database loaded! {len(databaseLocationsDictionary)} entries.\n')

print(f'Tweet Data:\n')

time.sleep(1)

try:
    # Main loop that processes each tweet
    for info in reversed(tweets):

        # Declared variables that need to be reset every loop
        tweetType = ''
        tweetParticipant = ''
        tweetLocation = ''
        tweetDirection = ''
        tweetTime = ''
        tweetDate = ''
        tweetLane = ''
        tweetID = ''
        tweetText = ''
        tweetLatitude = ''
        tweetLongitude = ''
        checkLocationAdded = False
        checkDuplicate = False
        checkAlert = False
        userBreak = False

        # Only look at their MMDA ALERT tweets
        if 'MMDA ALERT' in info.text.upper():

            checkAlert = True

            # Check if Tweet is duplicate from database
            tweetID = 'https://twitter.com/mmda/status/' + str(info.id)
            if tweetID in lstDuplicateCheck:
                print('Duplicate Data! Skipping to next tweet.')
                checkDuplicate = True
                continue
            else:
                tweetCounter += 1
                # Get date and text
                # Convert raw time from Twitter to GMT+8
                tweetDate = str(info.created_at)
                tweetDate = datetime.strptime(tweetDate, "%Y-%m-%d %H:%M:%S")
                tweetDate = tweetDate + timedelta(hours=8)
                tweetDate = str(tweetDate).split(' ')[0]

                tweetText = info.text
                tweetText = tweetText.replace('  ', ' ')
                info = info.text.upper()
                lstTweets.append(info)

                print('------------------------------------------------------')
                print(f'Tweet: {info}')
                print(f'Date: {tweetDate}')
                print(f'URL: {tweetID}')

                # Call on the TweetParse class
                twt = TweetParse(tweetText)
                tweetTime = twt.time(tweetText)
                tweetType = twt.inc_type(tweetText)
                tweetLane = twt.lane(tweetText)

                # Get location, participants, and direction
                pattern = re.compile(r' AT\s[a-zA-Z\Ñ\'\.\,\-0-9\/\s]+(AS OF)')
                matches = pattern.finditer(tweetText.upper())
                for match in matches:
                    tweetLocation = match.group(0)
                    # Location String Cleaning
                    tweetLocation = location_string_clean(tweetLocation)

                    # ELLIPTICAL ROAD in QC can confuse parser sometimes
                    if 'ELLIPTICAL' not in tweetLocation:
                        # Get direction then remove direction
                        # tweetLocation = twt.strip_direction(tweetText)
                        pattern = re.compile(r'( SB | NB | WB | EB )')
                        matches = pattern.finditer(info)
                        for match in matches:
                            tweetDirection = match.group(0)
                            tweetDirection = tweetDirection.replace(' ', '')
                            tweetLocation = tweetLocation.replace(' NB', '')
                            tweetLocation = tweetLocation.replace(' EB', '')
                            tweetLocation = tweetLocation.replace(' SB', '')
                            tweetLocation = tweetLocation.replace(' WB', '')
                        print(f'Direction: {tweetDirection}')
                        # print(f'DEBUG: CHECKPOINT1-{tweetLocation}')

                        # Get participants
                        if len(tweetLocation.split(' INVOLVING')) > 1:
                            # print(f'DEBUG: CHECKPOINT1.1-{tweetLocation}')
                            tweetParticipant = tweetLocation.split(' INVOLVING')[1]
                            tweetParticipant = tweetParticipant.rstrip(' ')
                            tweetParticipant = tweetParticipant.lstrip(' ')
                            if len(tweetParticipant) > 0:
                                print(f'Participants: {tweetParticipant}')
                                tweetLocation = tweetLocation.split('INVOLVING')[0].strip(' ')
                            print(f'Location: {tweetLocation}')

                        # Consider deletion
                        # Direction given. NO INVOLVED
                        if len(tweetLocation.split(' INVOLVING')) < 1:
                            print(f'DEBUG: CHECKPOINT2.1-{tweetLocation}')
                            tweetParticipant = tweetLocation.split(' AS OF ')[0]
                            tweetParticipant = tweetParticipant.rstrip(' ')
                            tweetParticipant = tweetParticipant.lstrip(' ')
                            print(f'Participants: {tweetParticipant}')

                    if 'ELLIPTICAL' in tweetLocation:

                        if 'ELLIPTICAL' and 'NORTH' in tweetLocation:
                            tweetLocation = 'ELLIPTICAL ROAD NORTH AVE.'
                        elif 'ELLIPTICAL' and 'QUEZON' in tweetLocation:
                            tweetLocation = 'ELLIPTICAL ROAD QUEZON AVE.'
                        elif 'ELLIPTICAL' and 'VISAYAS' in tweetLocation:
                            tweetLocation = 'ELLIPTICAL ROAD VISAYAS AVE.'
                        elif 'ELLIPTICAL' and 'EAST AVE' in tweetLocation:
                            tweetLocation = 'ELLIPTICAL ROAD EAST AVE.'
                        elif 'ELLIPTICAL' and ' DAR ' in tweetLocation:
                            tweetLocation = 'ELLIPTICAL ROAD DAR'
                        else:
                            pass
                            # tweetLocation = input('Enter elliptical road location:')
                        # tweetParticipant = input('TEMPORARY. Enter participants:')
                        # Get participants

                        pattern = re.compile(r'( SB | NB | WB | EB )')
                        matches = pattern.finditer(info)
                        for match in matches:
                            tweetDirection = match.group(0)
                            tweetDirection = tweetDirection.replace(' ', '')
                            tweetLocation = tweetLocation.replace(' NB', '')
                            tweetLocation = tweetLocation.replace(' EB', '')
                            tweetLocation = tweetLocation.replace(' SB', '')
                            tweetLocation = tweetLocation.replace(' WB', '')

                        if len(info.upper().split(' INVOLVING ')) > 1:
                            tweetParticipant = info.upper()
                            tweetParticipant = tweetParticipant.split(' INVOLVING')[1]
                            tweetParticipant = tweetParticipant.split(' AS OF ')[0]
                            tweetParticipant = tweetParticipant.rstrip(' ')
                            tweetParticipant = tweetParticipant.lstrip(' ')

                            tweetLocation = tweetLocation.upper()
                            tweetLocation = tweetLocation.split(' INVOLVING')[0]
                            tweetLocation = tweetLocation.split(' AT ')[0]
                            tweetLocation = tweetLocation.rstrip()
                            tweetLocation = tweetLocation.lstrip()

                        else:
                            # No participants mentioned in elliptical incident
                            tweetLocation = info.upper()
                            tweetLocation = tweetLocation.split(' AT ')[1]
                            tweetLocation = tweetLocation.split(' AS OF ')[0]
                            tweetLocation = tweetLocation.rstrip(' ')
                            tweetLocation = tweetLocation.lstrip(' ')

                        # print(f'DEBUG: tweetLocation is {tweetLocation}')
                        print(f'Participants: {tweetParticipant}')
                        print(f'Location: {tweetLocation}')
                        print(f'Direction: {tweetDirection}')

                # Special case. Get participants
                if 'STALLED' in info:
                    tweetParticipant = twt.stall(tweetText)

                # Special case. Get location and participants
                if 'RALLYIST' in info:
                    tweetType = 'RALLYIST'
                    # Get location and participants
                    tweetLocation = twt.rally_location(tweetText)
                    tweetParticipant = twt.rally_participants(tweetText)

        # Check for userBreak
        if tweetLocation == 'BREAK':
            userBreak = True
            break

        if checkAlert == True:
            # Check location with database
            # Declare variable to control while loop
            checkUserLocationChoice = False
            # empty variable
            #user_error = False
            while checkUserLocationChoice == False:
                try:
                    tweetLatitude = databaseLocationsDictionary[tweetLocation].split(',')[0]
                    tweetLongitude = databaseLocationsDictionary[tweetLocation].split(',')[1]
                    print(f'Latitude: {tweetLatitude}')
                    print(f'Longitude: {tweetLongitude}')
                    # Location is already added. Set check states to true
                    checkLocationAdded = True
                    checkUserLocationChoice = True

                except KeyError:
                    # User input to check if location string is correct
                    # if it is correct, type YES to add it, if not, type NO to manual fix

                    print(f'\nNew location detected! "{tweetLocation}" is not recognized.')
                    print(f'\nChoose number from list:')
                    print('1 - Add new location and new coordinates')
                    print(f'2 - Add new location based on existing coordinates\n')

                    userLocationChoice = input('Enter number to proceed:')

                    # While loop to check location
                    # The check variable is if the user's location is valid
                    # If valid, break out of while loop
                    while checkLocationAdded == False and checkUserLocationChoice == False:

                        userReset = False

                        if userLocationChoice == 'BREAK':
                            userBreak = True
                            break

                        elif userLocationChoice == '1':
                            print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
                            userInputCoord = input('Enter coordinates:')
                            userInputCoord = userInputCoord.replace(' ', '')
                            tweetLatitude = userInputCoord.split(',')[0]
                            tweetLongitude = userInputCoord.split(',')[1]
                            # print(f'DEBUG: userInputCoord is {userInputCoord}')
                            # print(f'DEBUG: tweetLatitude is {tweetLatitude}')
                            # print(f'DEBUG: tweetLatitude is {tweetLongitude}')
                            print(f'\nData to be added:')
                            print(
                                f'Location: {tweetLocation}\nLatitude: {tweetLatitude}\nLongitude: {tweetLongitude}')
                            userAppendLocationDatabase = input(
                                'Confirm information is correct? (Y/N)').upper()

                            # Y - Append to loc_database dictionary
                            if userAppendLocationDatabase == 'Y':
                                databaseLocationsDictionary[tweetLocation] = tweetLatitude + \
                                    ',' + tweetLongitude
                                checkUserLocationChoice = True
                                checkLocationAdded = True

                            elif userAppendLocationDatabase == 'N':
                                break

                            elif userAppendLocationDatabase == 'BREAK':
                                userBreak = True
                                break

                        elif userLocationChoice == '2':
                            userSearch = input('Search database for existing location: ').upper()
                            if userSearch == 'BREAK':
                                userBreak = True
                                break

                            print(f'Search results with {userSearch}')

                            # Get match to dictionary location
                            for idx, loc in enumerate(databaseLocationsDictionary):
                                if userSearch in loc:
                                    print(idx, loc)
                                    # UserSearchStringMatch = loc
                            print('Type "RESET" to search again.')
                            userInputCoordMatch = input('Choose index number: ')
                            if userInputCoordMatch == 'BREAK':
                                userBreak = True
                                break
                            if userInputCoordMatch == 'RESET':
                                userInputCoordMatch = ''
                                userSearch = ''
                                userInputCoord = ''
                                tweetLatitude = ''
                                tweetLongitude = ''
                                userLocationChoice = ''
                                userAppendLocationDatabase = ''
                                userReset = True
                                print('Enter details again.')
                                break

                            for idx, item in enumerate(databaseLocationsDictionary.items()):
                                if idx == int(userInputCoordMatch):
                                    print(idx, item)
                                    tweetLatitude = item[1].split(',')[0]
                                    tweetLongitude = item[1].split(',')[1]

                            print(
                                f'Data to be added:\nLocation: {tweetLocation}\nLatitude: {tweetLatitude}\nLongitude: {tweetLongitude}')
                            userAppendLocationDatabase = input(
                                'Confirm information is correct? (Y/N) ').upper()

                            # APPEND NEW INFO BASED ON EXISTING COORDS
                            if userAppendLocationDatabase == 'Y':
                                userInputCoordMatch = tweetLatitude + ',' + tweetLongitude
                                databaseLocationsDictionary[tweetLocation] = userInputCoordMatch
                                checkLocationAdded = True
                                checkUserLocationChoice = True
                            elif userAppendLocationDatabase == 'N':
                                userInputCoordMatch = ''
                                userSearch = ''
                                userInputCoord = ''
                                tweetLatitude = ''
                                tweetLongitude = ''
                                userLocationChoice = ''
                                userAppendLocationDatabase = ''
                                userReset = True
                                print('Enter details again.')
                                break

                        else:
                            # Break out of the current while loop
                            # to start process again
                            userInputCoordMatch = ''
                            userSearch = ''
                            userInputCoord = ''
                            tweetLatitude = ''
                            tweetLongitude = ''
                            userLocationChoice = ''
                            userAppendLocationDatabase = ''
                            userReset = True
                            print('Enter details again.')

                            if userAppendLocationDatabase == 'BREAK':
                                userBreak = True
                                break

                            if tweetLocation == 'BREAK':
                                userBreak = True
                                break
                        # EXIT OUT OF TRY LOOP HERE
                        if userReset == True:
                            break

                    if userBreak == True:
                        break

                    if checkLocationAdded == False and userReset == False:
                        tweetLatitude = databaseLocationsDictionary[tweetLocation].split(',')[0]
                        tweetLongitude = databaseLocationsDictionary[tweetLocation].split(',')[1]
                        print(f'Latitude: {tweetLatitude}')
                        print(f'Longitude: {tweetLongitude}')
                        checkUserLocationChoice = True

                if userBreak == True:
                    break

        if userBreak == True:
            break

        # If it is not a duplicate then write to CSV
        if checkDuplicate == False:

            WriteCombinedDict = {'Date': tweetDate, 'Time': tweetTime, 'Location': tweetLocation, 'Latitude': tweetLatitude,
                                 'Longitude': tweetLongitude, 'Direction': tweetDirection, 'Type': tweetType,
                                 'Lanes Blocked': tweetLane, 'Involved': tweetParticipant, 'Tweet': tweetText,
                                 'Source': tweetID}

            keys = WriteCombinedDict.keys()

            if tweetID not in lstDuplicateCheck:

                with open(databaseMain, 'r', newline='') as csv_file:
                    reader = csv.reader(csv_file)
                    try:
                        header_check = next(reader)
                    except StopIteration:
                        header_check = []

                    if header_check != []:
                        # Update version in main script folder
                        with open(databaseMain, 'a', newline='', encoding='utf-8') as CsvFile:
                            dict_writer = csv.DictWriter(CsvFile, keys)
                            dict_writer.writerow(WriteCombinedDict)
                    else:
                        # Then this is just an empty CSV file so we use write
                        print(f'\nNo data in the CSV! Adding header to CSV file')
                        with open(databaseMain, 'w', newline='', encoding='utf-8') as CsvFile:
                            dict_writer = csv.DictWriter(CsvFile, keys)
                            dict_writer.writeheader()
                            dict_writer.writerow(WriteCombinedDict)

except Exception as error:
    traceback.print_exc()
    config.arcpy_prevent_parser_error()
    exit()

if userBreak == True:
    print('User terminated script.')
    config.arcpy_prevent_parser_error()
    exit()

if tweetCounter == 0:
    print(f'\nNo new tweets!\n')
    config.arcpy_prevent_empty_input()
    exit()

print(f'\nUpdating location database...')

databaseLocationsFile = open(databaseLocations, 'w')
for x, y in databaseLocationsDictionary.items():
    databaseLocationsFile.writelines(x + '/' + y + '\n')
databaseLocationsFile.close()

# Drop empty rows generated
# Clean data for ArcGIS
df_1 = pd.read_csv(databaseMain)

df_1['Longitude'] = df_1['Longitude'].astype(str)
df_1['Longitude'] = df_1['Longitude'].str.rstrip(' ')
df_1['Longitude'] = df_1['Longitude'].str.replace('\t', '')
df_1['Longitude'] = df_1['Longitude'].str.replace('\n', '')
df_1.replace('None', np.nan, inplace=True)
df_1.dropna(axis=0, subset=['Source'], inplace=True)
df_1.to_csv(databaseMain, index=False)

# Update dataset in GIS workspace
copy(databaseMain, databaseGIS)

print(f'Twitter analysis finished.')
print(f'Analyzed {tweetCounter} new tweets')
print(f'Executing ArcPy script... This may take a few minutes depending on your computer\n')
