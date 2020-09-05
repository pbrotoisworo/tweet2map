

def check_duplicate_tweets(tweet_database=None, max_tweets=200):
    """
    Load last set of tweets to check for duplicates
    """
    lstDuplicateCheck = []

    try:
        with open(tweet_database, 'r', newline='') as CsvFile:
            reader = csv.reader(CsvFile)

            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    # print('Duplicate check initialized')
                    break

    except FileNotFoundError:
        print('CSV file not detected. Creating new CSV file')
        with open(tweet_database, 'x', newline='') as CsvFile:
            # reader = csv.reader(CsvFile)
            for idx, row in enumerate(reversed(list(CsvFile))):
                dataRow = row
                dataRow = dataRow.replace('\r\n', '')
                lstDuplicateCheck.append(dataRow.split(',')[-1])
                if idx == max_tweets:
                    break

    return lstDuplicateCheck