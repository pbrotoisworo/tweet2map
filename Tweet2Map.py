# Encoding: utf-8

print('MMDA Tweet2Map Version 0.9')
print('Panji P. Brotoisworo')
print('Contact: panji.p.broto@gmail.com')
print('Website: https://panjib.wixsite.com/blog/mmdatweet2map')
print(f'\nInitializing Libraries...')

import re
import time
from modules.function_list import location_string_clean
from modules.TweetParse import TweetParse
from modules.RunConfig import *
from modules.initialization import *
from modules.dbmanage import *
from modules.geoanalysis import *
import modules.logging
from shutil import copy
import pandas as pd
from datetime import datetime, timedelta
import traceback
import logging
import numpy as np
import geopandas
from shapely.geometry import Point

# Load scripts from modules.initialization
config = RunConfig('config.ini')
config.reset_errors()

# Declare variables
databaseLocationsDictionary = {}
lstTweets = []
lstDuplicateCheck = []
userBreak = False
userClose = False
tweetCounter = 0
dfAppendList = []

# Load database
try:
    config.dir_databases()
    databaseMain = config.dir_databases()[0]
    databaseGIS = config.dir_databases()[1]
    database_no_null = config.dir_databases()[2]
except PermissionError:
    print('Permission Error. Please check if file is in use')
    time.sleep(5)
    exit()

databaseLocations = r'modules\dictionary_database.txt'
# databaseMain = 'data_mmda_traffic_alerts.csv'
# database copy in my GIS folder
#databaseGIS = r'C:\GIS\Data Files\Work Files\MMDA Tweet2Map\input\data_mmda_traffic_alerts.csv'

print('Connecting to API...')
tweets = initialization_tweepy_connect(input_consumer_key=config.tweepy_tokens()[0],
                                       input_consumer_secret=config.tweepy_tokens()[1],
                                       input_access_token=config.tweepy_tokens()[2],
                                       input_access_secret=config.tweepy_tokens()[3])
# TO DO: TRIGGER PREVENT PARSER ERROR IF MODULE CANNOT CONNECT
if len(tweets) == 0:
    config.arcpy_prevent_parser_error()
    exit()

# Logging
modules.logging.logger('INFO')

# Load database of string locations
print(f'Loading database...\n')
try:
    databaseLocationsDictionary = dbmanage_load_location_data(databaseLocations)
except:
    traceback.print_exc()
    config.arcpy_prevent_parser_error()
    exit()

# Load last tweets to prevent duplicate writes to the tweet database
lstDuplicateCheck = initialization_check_duplicate(tweet_database=databaseMain,
                                                   max_tweets=200)

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

                logging.info(f'tweetID = {str(tweetID)}')
                logging.info(f'info.text.upper() = {info}')
                logging.info(f'tweetText = {tweetText}')

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
                        pattern = re.compile(r'( SB | NB | WB | EB | SB| NB| WB| EB)')
                        #matches = pattern.finditer(info)
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
                        print(f'Direction: {tweetDirection}')
                        logging.debug(f'CHECKPOINT1-{tweetLocation}')

                        # Get participants
                        if len(tweetLocation.split(' INVOLVING')) > 1:
                            logging.debug('DEBUG: CHECKPOINT1.1-{}'.format(tweetLocation))
                            tweetParticipant = tweetLocation.split(' INVOLVING')[1]
                            tweetParticipant = tweetParticipant.rstrip(' ')
                            tweetParticipant = tweetParticipant.lstrip(' ')
                            if len(tweetParticipant) > 0:
                                print(f'Participants: {tweetParticipant}')
                                tweetLocation = tweetLocation.split('INVOLVING')[0].strip(' ')
                            print(f'Location: {tweetLocation}')
                        else:
                            print(f'Location: {tweetLocation}')

                        # Consider deletion
                        # Direction given. NO INVOLVED
                        if len(tweetLocation.split(' INVOLVING')) < 1:
                            logging.debug('DEBUG: CHECKPOINT2.1-{}'.format(tweetLocation))
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
                            tweetLocation = tweetLocation.replace(' NB ', ' ')
                            tweetLocation = tweetLocation.replace(' EB ', ' ')
                            tweetLocation = tweetLocation.replace(' SB ', ' ')
                            tweetLocation = tweetLocation.replace(' WB ', ' ')
                            tweetParticipant = tweetParticipant.rstrip(' ')
                        logging.debug(f'DEBUG: CHECKPOINT3-{tweetLocation}')

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

        if len(tweetLocation) > 50:
            logging.warning('Possible location error \ntweetLocation: {}'.format(tweetLocation))

        # Check for userBreak
        if tweetLocation == 'BREAK':
            userBreak = True
            break

        if checkAlert == True:
            # Check location with database
            # Declare variable to control while loop
            checkUserLocationChoice = False
            # empty variable
            # user_error = False
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

                    # Show probable similar locations
                    # similarList = dbmanage_check_similar_locations(tweetLocation, databaseLocations)
                    # print('\nSimilar locations:')
                    # for x in similarList:
                    #     print(x)

                    # User input to check if location string is correct
                    # if it is correct, type YES to add it, if not, type NO to manual fix

                    print(f'\nNew location detected! "{tweetLocation}" is not recognized.')
                    print(f'\nChoose number from list:')
                    print('1 - Add new location and new coordinates')
                    print(f'2 - Add new location based on existing coordinates')
                    print(f'3 - Fix location name\n')

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
                        elif userLocationChoice == '3':
                            tweetLocation = input('Input new location: ').upper()
                            userReset = True

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

            if len(tweetLatitude) and len(tweetLongitude) > 0:
                tweetCounter += 1

            WriteCombinedDict = {'Date': tweetDate, 'Time': tweetTime, 'Location': tweetLocation, 'Latitude': tweetLatitude,
                                 'Longitude': tweetLongitude, 'Direction': tweetDirection, 'Type': tweetType,
                                 'Lanes Blocked': tweetLane, 'Involved': tweetParticipant, 'Tweet': tweetText,
                                 'Source': tweetID}

            keys = WriteCombinedDict.keys()

            if tweetID not in lstDuplicateCheck and len(tweetID) > 0:

                dfAppendList.append(WriteCombinedDict)

                # try:
                #     dbmanage_update_csv_data(databaseMain, WriteCombinedDict, keys)
                # except PermissionError:
                #     print(f'Permission Error encountered. Please check if database file is in use.')
                #     print(f'Database file: {databaseMain}')
                #     time.sleep(5)
                #     exit()

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

# Update Database
print(f'\nUpdating databases...')
dbmanage_update_csv_data(databaseMain, dfAppendList)

databaseLocationsFile = open(databaseLocations, 'w')
for x, y in databaseLocationsDictionary.items():
    databaseLocationsFile.writelines(x + '/' + y + '\n')
databaseLocationsFile.close()

# Drop empty rows generated
# Clean data for ArcGIS
dbmanage_clean_tweet_data(databaseMain)

# Get new database size
df_count = dbmanage_database_count(databaseMain)

# Generate separate dataframe for spatial join
# Then drop nulls for spatial join
# Load and prep excel file
print('Executing spatial join...')

crs = {'init': 'espg:4326'}
df = pd.read_csv(databaseMain)
df.replace(to_replace='None', value=np.nan, inplace=True)
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
df['Longitude'] = df['Longitude'].astype('float64')
df['Latitude'] = df['Latitude'].astype('float64')
df['geometry'] = df.apply(lambda x: Point((float(x['Longitude']), float(x['Latitude']))), axis=1)

# Load shapefile
shapefile = geopandas.read_file(r'shapefiles\boundary_ncr.shp')
shapefile.drop(['GID_0', 'GID_1', 'NL_NAME_1', 'GID_2', 'VARNAME_2', 'NL_NAME_2', 'TYPE_2', 'NAME_0',
                'NAME_1', 'ENGTYPE_2', 'CC_2', 'HASC_2'], axis=1, inplace=True)
shapefile.crs = {'init': 'epsg:4326'}

# Join
df = geopandas.GeoDataFrame(df, crs=crs, geometry='geometry')
df.crs = {'init': 'epsg:4326'}

# Spatial Join
df_gpd = geopandas.sjoin(df, shapefile, how='left', op='within')
df_gpd.drop(['index_right', 'geometry'], axis=1, inplace=True)
df_gpd.rename(columns={'NAME_2': 'City'}, inplace=True)
df_gpd = df_gpd[['Date', 'Time', 'City', 'Location', 'Latitude', 'Longitude', 'Direction',
                 'Type', 'Lanes Blocked', 'Involved', 'Tweet', 'Source']]
df_gpd.to_csv(database_no_null, index=False)


#df.to_csv(r'C:\Users\Panji\Documents\Python Scripts\Projects\MMDA Tweet2Map\backup\data_mmda_traffic_alerts - Copy.csv', index=False)
# df_no_null = geoanalysis_spatial_join(df, shapefile=r'shapefiles\boundary_ncr.shp')
# df_no_null.to_csv(database_no_null, index=False)

# Update dataset in GIS workspace
copy(database_no_null, databaseGIS)

print(f'\nTwitter analysis finished.')
print(f'Analyzed {tweetCounter} new tweets')
print(f'Current database size: {df_count}\n')

try:
    program_exit = str(input('Press ENTER to close'))
except:
    exit()
exit()
