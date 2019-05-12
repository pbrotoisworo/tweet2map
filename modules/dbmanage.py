import csv


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
