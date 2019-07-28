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
import sys

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
    sys.exit()

databaseLocations = r'modules\dictionary_database.txt'

print('Connecting to API...')
tweets = initialization_tweepy_connect(input_consumer_key=config.tweepy_tokens()[0],
                                       input_consumer_secret=config.tweepy_tokens()[1],
                                       input_access_token=config.tweepy_tokens()[2],
                                       input_access_secret=config.tweepy_tokens()[3])
# TO DO: TRIGGER PREVENT PARSER ERROR IF MODULE CANNOT CONNECT
if len(tweets) == 0:
    sys.exit()

# Logging
modules.logging.logger('INFO')

# Load database of string locations
print(f'Loading database...\n')
try:
    databaseLocationsDictionary = dbmanage_load_location_data(databaseLocations)
except:
    traceback.print_exc()
    print('Critical Error! Cannot load location database.')
    input('Press any button to continue...')
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

            logging.info('===================================================')
            logging.info('Tweet ID: {}'.format(tweetID))

            if tweetID in lstDuplicateCheck:
                print('Duplicate Data! Skipping to next tweet.')
                checkDuplicate = True
                logging.info('Duplicate data. Skipping.')
                continue
            else:

                logging.info('Processing Tweet {}'.format(str(tweetCounter)))

                tweetText = info.text
                tweetText = tweetText.replace('  ', ' ')
                lstTweets.append(info)

                # Create TweetParse object then parse tweet
                twt = TweetParse()
                tweetDate = twt.get_date(info)
                tweetTime = twt.get_time(tweetText)
                tweetType = twt.get_inc_type(tweetText)
                tweetLane = twt.get_lanes_blocked(tweetText)
                tweetDirection = twt.get_direction(tweetText)
                tweetParticipant = twt.get_participants(tweetText)
                tweetLocation = twt.get_location(tweetText)

                if 'RALLY' in tweetText.upper():
                    tweetLocation = twt.get_rally_location(tweetText)
                    tweetParticipant = twt.get_rally_participants(tweetText)
                    tweetType = 'RALLY'

                if 'STALLED' in tweetText.upper():
                    tweetParticipant = twt.get_stalled_participants(tweetText)
                    tweetType = 'STALLED'

                print('------------------------------------------------------')
                print(f'Tweet: {tweetText}')
                print(f'Date: {tweetDate}')
                print(f'Time: {tweetTime}')
                print(f'URL: {tweetID}')
                print(f'Incident Type: {tweetType}')
                print(f'Participants: {tweetParticipant}')
                print(f'Lanes Involved: {tweetLane}')
                print(f'Location: {tweetLocation}')

        # Check for userBreak
        if tweetLocation == 'BREAK':
            userBreak = True
            break

        if checkAlert == True:
            # Check location with database
            # Declare variable to control while loop
            checkUserLocationChoice = False
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
                    print(f'3 - Fix location name')
                    print(f'4 - Set location as invalid\n')

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
                            logging.info('MANUAL LOCAITON FIX FROM USER')
                            logging.info(f'\tOld Location: {tweetLocation}')
                            tweetLocation = input('Input new location: ').upper()
                            logging.info(f'\tRevised Location: {tweetLocation}')
                            userReset = True

                        elif userLocationChoice == '4':
                            # TESTING
                            tweetLatitude = ''
                            tweetLongitude = ''
                            userInputCoordMatch = tweetLatitude + ',' + tweetLongitude
                            databaseLocationsDictionary[tweetLocation] = userInputCoordMatch

                            print(
                                f'Data to be added:\nLocation: {tweetLocation}\nLatitude: {tweetLatitude}\nLongitude: {tweetLongitude}')
                            userAppendLocationDatabase = input(
                                'Confirm information is correct? (Y/N) ').upper()

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
    sys.exit()

if userBreak == True:
    print('User terminated script.')
    sys.exit()

if tweetCounter == 0:
    print(f'\nNo new tweets!\n')
    sys.exit()

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


# df.to_csv(r'C:\Users\Panji\Documents\Python Scripts\Projects\MMDA Tweet2Map\backup\data_mmda_traffic_alerts - Copy.csv', index=False)
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
