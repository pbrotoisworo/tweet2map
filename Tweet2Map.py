#Encoding: utf-8
import tweepy
import re
import time
import csv
import pandas as pd
from functions_list import *

print('MMDA Tweet2Map Version 0.5')
print('Panji Brotoisworo')
print('E-mail: panji.p.broto@gmail.com')
print('Website: https://panjib.wixsite.com')
print(f'\nStarting application...\n')

time.sleep(2)

DatabaseLocationStrings = {}
ListDirection = ['NB','SB','EB','WB']
ListDirectionCheck = [' NB ', ' SB ', ' EB ', ' WB ']
ListTweets = []
ListDuplicateCheck = []
UserBreak = False
FileLocations = 'dictionary_database.txt'
FileDataset = 'data_mmda_traffic_alerts.csv'

# Load database of string locations or create one if it doesn't exist
try:
    f_DBLocationStrings = open(FileLocations,'r')
    for line in f_DBLocationStrings:
        x = line.split("/")
        x[1] = x[1].replace('\n','')
        x[1] = x[1].replace(' ','')
        DatabaseLocationStrings[x[0]] = x[1]
    f_DBLocationStrings.close()
except FileNotFoundError:
    print('Database not detected. Creating new txt file')
    # Create file for read and write
    f_DBLocationStrings = open(FileLocations,'x+')
        
# Load last set of tweets to check for duplicates
try:
    with open(FileDataset,'r',newline='') as CsvFile:
        #print('Writing to CSV File')
        reader = csv.reader(CsvFile)

        for idx, row in enumerate(reversed(list(CsvFile))):
            DataRow = row
            DataRow = DataRow.replace('\r\n','')
            ListDuplicateCheck.append(DataRow.split(',')[-1])
            if idx == 200:
                break
        
except FileNotFoundError:
    print('CSV file not detected. Creating new CSV file')
    with open(FileDataset,'x',newline='') as CsvFile:
        #reader = csv.reader(CsvFile)
        for idx, row in enumerate(reversed(list(CsvFile))):
            DataRow = row
            DataRow = DataRow.replace('\r\n','')
            ListDuplicateCheck.append(DataRow.split(',')[-1])
            if idx == 200:
                break

print(f'Location Database loaded! {len(DatabaseLocationStrings)} entries.\n')
print(f'Tweet Data:\n')

# Tweepy Settings
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
tweets = api.user_timeline(screen_name="mmda",count=200,include_rts=False)

# Code that will analyze each tweet
for info in reversed(tweets):
    
    # Declared variables that need to be reset every loop
    TwtType = ''
    TwtParticipant = ''
    TwtLocation = ''
    TwtDirection = ''
    TwtTime = ''
    TwtDate = ''
    TwtLane = ''
    TwtId = ''
    TwtText = ''
    TwtType = ''
    TwtLatitude = ''
    TwtLongitude = ''
    LocationAddCheck = False
    
    # Only look at their MMDA ALERT tweets
    if 'MMDA ALERT' in info.text.upper():
        
        # Get post ID and check if it is a duplicate tweet
        TwtId = 'https://twitter.com/mmda/status/' + str(info.id)
        if TwtId in ListDuplicateCheck:
            print('Duplicate Data! Skipping to next tweet.')
            continue
        else:
            # Get date and text
            TwtDate = info.created_at
            TwtDate = TwtDate.strftime("%m-%d-%Y")
            TwtText = info.text
            info = info.text.upper()
            ListTweets.append(info)

            print('-------------------------------')
            print(f'Tweet: {info}')
            print(f'Date: {TwtDate}')
            print(f'URL: {TwtId}')

            # Get type
            pattern = re.compile(r'MMDA ALERT: [A-Za-z0-9\s]+AT ')
            matches = pattern.finditer(info)
            for match in matches:
                TwtType = match.group(0)
                TwtType = TwtType.replace('MMDA ALERT: ','')
                TwtType = TwtType.replace(' AT ','')
            print(f'Type: {TwtType}')
                
            # Get location, participants, and direction
            pattern = re.compile(r'AT\s[a-zA-Z\Ñ\'\.\,\-0-9\/\s]+(AS OF)')
            matches = pattern.finditer(info)
            for match in matches:
                TwtLocation = match.group(0)
                # Location String Cleaning
                string_clean(TwtLocation)
                
                # ELLIPTICAL ROAD in QC can confuse parser sometimes
                if 'ELLIPTICAL' not in TwtLocation:
                    # If there are participants INVOLVED, get the participants
                    if len(TwtLocation.split(' INVOLVING')) > 1:
                        TwtParticipant = TwtLocation.split(' INVOLVING')[1]
                        TwtParticipant = TwtParticipant.rstrip(' ')
                        TwtParticipant = TwtParticipant.lstrip(' ')
                        print(f'Participants: {TwtParticipant}')

                    # Get location
                    TwtLocation = TwtLocation.split('INVOLVING')[0].strip(' ')
                    #TwtDirection = TwtLocation.rsplit(' ',1)[1]
                    TwtLocation = TwtLocation.rsplit(' ',1)[0]
                    #print(f'DEBUG: Checkpoint Get Location')
                    print(f'Location: {TwtLocation}')
                    
                    # Get direction
                    #if len(TwtDirection) < 1 or TwtDirection not in ListDirectionCheck:
                    pattern = re.compile(r'( SB | NB | WB | EB )')
                    matches = pattern.finditer(info)
                    for match in matches:
                        TwtDirection = match.group(0)
                        TwtDirection = TwtDirection.replace(' ','')     
                    print(f'Direction: {TwtDirection}')

                if 'ELLIPTICAL' in TwtLocation:
                    
                    if 'ELLIPTICAL' and 'NORTH' in TwtLocation:
                        TwtLocation = 'ELLIPTICAL ROAD NORTH AVE.'
                    elif 'ELLIPTICAL' and 'QUEZON' in TwtLocation:
                        TwtLocation = 'ELLIPTICAL ROAD QUEZON AVE.'
                    elif 'ELLIPTICAL' and 'VISAYAS' in TwtLocation:
                        TwtLocation = 'ELLIPTICAL ROAD VISAYAS AVE.'
                    else:
                        TwtLocation = input('Enter location:')
                    #TwtParticipant = input('TEMPORARY. Enter participants:')
                    # Get participants
                    if len(TwtLocation.split(' INVOLVING')) > 1:
                        TwtParticipant = TwtLocation.split(' INVOLVING')[1]
                        TwtParticipant = TwtParticipant.rstrip(' ')
                        TwtParticipant = TwtParticipant.lstrip(' ')
                        print(f'Participants: {TwtParticipant}')
                    #print(f'DEBUG: TwtLocation is {TwtLocation}')
                    print(f'Participants: {TwtParticipant}')
                    print(f'Location: {TwtLocation}')
                    print(f'Direction: {TwtDirection}')

            if 'STALLED' in info:

                pattern = re.compile(r'STALLED [A-Z0-9\-\s]+DUE')
                matches = pattern.finditer(info)
                for match in matches:
                    TwtParticipant = match.group(0)
                    TwtParticipant = TwtParticipant.replace('STALLED ','')
                    TwtParticipant = TwtParticipant.replace(' DUE','')
                    TwtParticipant = TwtParticipant.rstrip(' ')
                    print(f'Participants: {TwtParticipant}')
            
            #Check location with database
            try:
                #print(f'DEBUG: TwtLocation is {TwtLocation}')
                TwtLatitude = DatabaseLocationStrings[TwtLocation].split(',')[0]
                TwtLongitude = DatabaseLocationStrings[TwtLocation].split(',')[1]
                print(f'Latitude: {TwtLatitude}')
                print(f'Longitude: {TwtLongitude}')
                LocationAddCheck = True

            except KeyError:
                #User input to check if location string is correct
                #if it is correct,, type YES to add it, if not, type NO to manual fix

                print(f'\nNew location detected! {TwtLocation} is not recognized.')
                print(f'\nChoose number from list:')
                print('1 - Add new location and new coordinates')
                print(f'2 - Add new location based on existing coordinates\n')
                #print(f'3 - Auto recommend (BETA)')

                UserLocChoice = input('Enter number to proceed:')

                # Declare variable to control while loop
                UserLocChoiceCheck = False

                while UserLocChoiceCheck == False:

                    if UserLocChoice == 'BREAK':
                        break

                    elif UserLocChoice == '1':
                        print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
                        UserInputCoord = input('Enter coordinates:')
                        UserInputCoord = UserInputCoord.replace(' ','')
                        TwtLatitude = UserInputCoord.split(',')[0]
                        TwtLongitude = UserInputCoord.split(',')[1]
#                           print(f'DEBUG: UserInputCoord is {UserInputCoord}')
#                           print(f'DEBUG: TwtLatitude is {TwtLatitude}')
#                           print(f'DEBUG: TwtLatitude is {TwtLongitude}')
                        print(f'\nData to be added:')
                        print(f'Location: {TwtLocation}\nLatitude: {TwtLatitude}\nLongitude: {TwtLongitude}')
                        UserAppendDatabaseLoc = input('Confirm information is correct? (Y/N)')

                        # Append to loc_ database dictionary
                        if UserAppendDatabaseLoc == 'Y':
                            DatabaseLocationStrings[TwtLocation] = TwtLatitude + ',' + TwtLongitude
                            UserLocChoiceCheck = True
                            LocationAddCheck = True
                        elif UserAppendDatabaseLoc == 'N':
                            continue
                        elif UserAppendDatabaseLoc == 'BREAK':
                            break

                    elif UserLocChoice == '2':
                        UserSearchInput = input('Search database for existing location: ').upper()
                        print(f'Search results with {UserSearchInput}')

                        # Get match to dictionary location
                        for idx,loc in enumerate(DatabaseLocationStrings): 
                            if UserSearchInput in loc:
                                print(idx,loc)
                                #UserSearchStringMatch = loc

                        UserSearchCoordMatch = input('Choose index number: ')

                        for idx,item in enumerate(DatabaseLocationStrings.items()):
                            if idx == int(UserSearchCoordMatch):
                                print(idx,item)
                                #print(f'item is {type(item)}')
                                TwtLatitude = item[1].split(',')[0]
                                TwtLongitude = item[1].split(',')[1]
                                #print(f'DEBUG: TwtLatitude is {TwtLatitude}')
                                #print(f'DEBUG: TwtLatitude is {TwtLongitude}')

                        print(f'Data to be added:\nLocation: {TwtLocation}\nLatitude: {TwtLatitude}\nLongitude: {TwtLongitude}')        
                        UserAppendDatabaseLoc = input('Confirm information is correct? (Y/N) ')

                        # APPEND NEW INFO BASED ON EXISTING COORDS
                        if UserAppendDatabaseLoc == 'Y':
                            UserSearchCoordMatch = TwtLatitude + ',' + TwtLongitude
                            DatabaseLocationStrings[TwtLocation] = UserSearchCoordMatch
                            LocationAddCheck = True
                            UserLocChoiceCheck = True
                        elif UserAppendDatabaseLoc == 'N':
                            pass
                    # elif UserLocChoice == '3':
                    #    pass

                    else:
                        print('Invalid input!')
                        print('Enter details again.')

                if TwtLocation == 'BREAK':
                    break

            if LocationAddCheck == False:
                TwtLatitude = DatabaseLocationStrings[TwtLocation].split(',')[0]
                TwtLongitude = DatabaseLocationStrings[TwtLocation].split(',')[1]
                print(f'Latitude: {TwtLatitude}')
                print(f'Longitude: {TwtLongitude}')

        # Get time
        pattern = re.compile(r'\d+\D\d\d[\s(AM|PM)]+\.')
        matches = pattern.finditer(info)
        for match in matches:
            TwtTime = match.group(0)
            TwtTime = TwtTime.replace('.','')
            if len(TwtTime) < 1:
                TwtTime = input('Manual correction needed! Input time: ')
                if TwtTime == 'BREAK':
                    break
            print(f'Time: {TwtTime}')

        # Get lane occupied
        pattern = re.compile(r'\d\s(LANE|LANES)')
        matches = pattern.finditer(info)
        for match in matches:
            TwtLane = match.group(0)
            TwtLane = TwtLane.split(' ')[0]
            if TwtLane == '':
                TwtLane = input('Manual correction needed! Input lanes blocked: ')
                if TwtLane == 'BREAK':
                    break

            print(f'Lanes Occupied: {TwtLane}')


    WriteCombinedDict = {'Date':TwtDate,'Time':TwtTime,'Location':TwtLocation,'Latitude':TwtLatitude,
                             'Longitude':TwtLongitude,'Direction':TwtDirection,'Type':TwtType,
                             'Lanes Blocked':TwtLane,'Involved':TwtParticipant,'Tweet':TwtText, 'Source':TwtId}

    keys = WriteCombinedDict.keys()

    with open ('data_mmda_traffic_alerts.csv','r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        try:
            header_check = next(reader)
        except StopIteration:
            pass
        if len(header_check) > 0:
            # There is data
            if TwtId not in ListDuplicateCheck:
                #print(f'TwtId is {TwtId}')
                with open('data_mmda_traffic_alerts.csv','a',newline='', encoding='utf-8') as CsvFile:
                    dict_writer = csv.DictWriter(CsvFile, keys)
                    dict_writer.writerow(WriteCombinedDict)
            else:
                print('Duplicate data! Skipping to next tweet.')
                continue

        else:
            # Then this is just an empty CSV file so we use write
            print(f'\nNo data in the CSV! Adding header to CSV file')
            with open('data_mmda_traffic_alerts.csv','w',newline='', encoding='utf-8') as CsvFile:
                dict_writer = csv.DictWriter(CsvFile, keys)
                dict_writer.writeheader()
                dict_writer.writerow(WriteCombinedDict)
            

print('Updating location database...')
f_DBLocationStrings = open('dictionary_database.txt','w')
for x,y in DatabaseLocationStrings.items():
#     print(x,y)
#     print(type(x),type(y))
    f_DBLocationStrings.writelines(x + '/' + y + '\n')
f_DBLocationStrings.close()

# Drop empty rows generated
df = pd.read_csv(FileDataset)
df.dropna(axis=0,subset=['Source'], inplace=True)
df.to_csv(FileDataset, index=False)

print('Tweet analysis finished.')
