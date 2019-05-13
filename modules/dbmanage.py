import csv
import pandas as pd
import numpy as np


def dbmanage_load_location_data(database_file=None):
    """
    Load location data and check it with latest tweets
    """
    databaseLocationsDictionary = {}

    with open(database_file, 'r') as f:
        for line in f:
            x = line.split("/")
            x[1] = x[1].replace('\n', '')
            x[1] = x[1].replace(' ', '')
            databaseLocationsDictionary[x[0]] = x[1]

    print(f'Location Database loaded! {len(databaseLocationsDictionary)} entries.\n')

    return databaseLocationsDictionary


def dbmanage_update_csv_data(tweet_database=None, write_row=None, keys=None):
    """
    Update CSV file row by row
    """
    with open(tweet_database, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        try:
            header_check = next(reader)
        except StopIteration:
            header_check = []

        if header_check != []:
            # Update version in main script folder
            with open(tweet_database, 'a', newline='', encoding='utf-8') as CsvFile:
                dict_writer = csv.DictWriter(CsvFile, keys)
                dict_writer.writerow(write_row)
        else:
            # Then this is just an empty CSV file so we use write
            print(f'\nNo data in the CSV! Adding header to CSV file')
            with open(tweet_database, 'w', newline='', encoding='utf-8') as CsvFile:
                dict_writer = csv.DictWriter(CsvFile, keys)
                dict_writer.writeheader()
                dict_writer.writerow(write_row)


def dbmanage_clean_tweet_data(tweet_database):
    df_1 = pd.read_csv(tweet_database)

    df_1['Longitude'] = df_1['Longitude'].astype(str)
    df_1['Longitude'] = df_1['Longitude'].str.rstrip(' ')
    df_1['Longitude'] = df_1['Longitude'].str.replace('\t', '')
    df_1['Longitude'] = df_1['Longitude'].str.replace('\n', '')
    df_1.replace('None', np.nan, inplace=True)
    df_1.dropna(axis=0, subset=['Source'], inplace=True)
    df_1.to_csv(tweet_database, index=False)


def dbmanage_check_similar_locations(tweet_location, location_database):
    """
    tweet_location: The location string
    location_database: The file containing the names and coords of locations
    """

    #tweetLocation = 'EDSA ORTIGAS FLYOVER JULIA'

    # Automate getting the word count which will count as the index
    # Split and get word count
    tweetLocationSplit = tweet_location.split(' ')
    search_cap = len(tweetLocationSplit)

    # Create a dictionary of all the individual words/search terms
    search_words = {}
    for x in range(0, search_cap):
        search_words[x] = tweetLocationSplit[x]

    searchOutput_step0 = []
    searchOutput_step1 = []
    searchOutput_step2 = []
    searchOutput_step3 = []
    searchOutput_step4 = []
    searchOutput_step5 = []
    searchOutput_else = []

    # list of locations from location database
    with open(location_database, 'r') as f:
        line = f.readlines()
        for x in line:
            searchOutput_step0.append(x)

    for idx in range(0, search_cap):

        searchTerm1 = tweetLocationSplit[0]
        if idx < search_cap:
            searchTerm2 = tweetLocationSplit[idx + 1]

        counter_hit = 0

        for x in searchOutput_step1:
            if searchTerm and searchTerm2 in x:
                counter_hit += 1
                if idx == 0:
                    searchOutput_step0.append(x)
                elif idx == 1:
                    searchOutput_step1.append(x)
                elif idx == 2:
                    searchOutput_step2.append(x)
                elif idx == 3:
                    searchOutput_step3.append(x)
                elif idx == 4:
                    searchOutput_step4.append(x)
                elif idx == 5:
                    searchOutput_step5.append(x)
                else:
                    searchOutput_else.append(x)
        print('\nBlock {}. Matched {}'.format(idx, counter_hit))

        # search in all the lists
        combinedList = [searchOutput_step1, searchOutput_step2,
                        searchOutput_step3, searchOutput_step4,
                        searchOutput_step5, searchOutput_else]
        locationList = []
        matchDictionary = {}
        matchList = []
        outputList = []

        # combinedList[0]

        # Create word list containing output words from all lists
        for group in combinedList:
            if len(group) > 0:
                for location in group:
                    locationList.append(location)

        # Create match list where each hit on a word will add 1 to a counter,
        # thus the higher the number the higher the likelihood
        # of it being the ideal match
        for x in locationList:
            if x in matchDictionary:
                matchDictionary[x] += 1
            else:
                matchDictionary[x] = 0

        # Create a list where each item is structured as such:
        # [NUMBER OF HITS LOCATION STRING]
        # This is so the list can be sorted numerically which will show the top hits
        for location in matchDictionary:
            matchList.append('{} {}'.format(matchDictionary[location], location))

        for x in sorted(matchList):
            if int(x[0]) > 1:
                x = x.split(' ')[1]
                x = ' '.join(x)
                outputList.append(x)

        return outputList
