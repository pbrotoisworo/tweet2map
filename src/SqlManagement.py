import sqlite3
import pandas as pd
import geopandas
import os
from shapely.geometry import Point


class Tweet2MapDatabaseSQL:
    """Object based management of SQL Database"""

    SQL_TABLE = 'INCIDENTS'

    def __init__(self, sql_database_file=None, num_latest_tweets=200, verbose=False):

        self.sql_database_file = sql_database_file

        # If empty, create default database
        if not os.path.exists(sql_database_file):
            default_new_database = os.path.join('data', 'data.sqlite')
            if not os.path.exists('data'):
                # Make folder if not existing
                os.mkdir('data')
            if verbose:
                print(f'WARNING: SQL database not detected. Creating new database: {default_new_database}')
            self.sql_database_file = sql_database_file = default_new_database
            conn = sqlite3.connect(self.sql_database_file)
            cols = ['Date', 'Time', 'City', 'Location', 'Latitude' ,'Longitude', 'High_Accuracy', 'Direction',
                    'Type', 'Lanes_Blocked', 'Involved', 'Tweet', 'Source']
            df = pd.DataFrame(columns=cols)
            df.to_sql(name=self.SQL_TABLE, con=conn)
            conn.close()

        self.conn = sqlite3.connect(self.sql_database_file)
        self.c = self.conn.cursor()
        self.num_columns = self.conn.execute(
            'SELECT * FROM {} LIMIT 1'.format(self.SQL_TABLE))
        self.num_columns = len([col[0] for col in self.num_columns.description])
        self.columns = self.conn.execute('SELECT * FROM {} LIMIT 1'.format(self.SQL_TABLE))
        self.columns = [col[0] for col in self.columns.description]
        self.row_count = len(pd.read_sql_query(f'SELECT * FROM {self.SQL_TABLE}', self.conn))
        
        self.num_latest_tweets = num_latest_tweets
        if self.num_latest_tweets > self.row_count:
            raise Exception(f'Number of latest tweets to check "{self.num_latest_tweets}" > rows in database "{self.row_count}"')

    def load_latest_tweets(self):
        df = pd.read_sql_query(
            "select Source from {} WHERE Date <= date('now') AND Date >=  date('now', '-2 day')".format(self.SQL_TABLE), self.conn)
        latest_values = list(df.values.flatten())
        return latest_values

    def get_newest_tweet_ids(self):
        """Gets the last n Tweets to prevent duplicates when processing new Tweepy data"""

        # Get original tweets from existing database
        df = pd.read_sql_query(f'SELECT * FROM {self.SQL_TABLE} ORDER BY date(Date) DESC LIMIT {self.num_latest_tweets}', self.conn)
        id_list = list(df['Source'])
        # Remove URL and extract just the ID
        id_list = [str(x.replace('https://twitter.com/mmda/status/', '')) for x in id_list]
        
        return id_list

    def close_connection(self):
        """Close SQL database connection"""
        self.c.close()
        self.conn.close()

    def spatial_join(self, sql_cmd_values):
        """Input of sql_cmd_values is list containing column values"""

        column_join = self.columns
        if 'City' in column_join:
            column_join.remove('City')

        df = pd.DataFrame([sql_cmd_values], columns=column_join)

        # if ((len(str(df.iloc[0]['Latitude'])) != 0) or (df.iloc[0]['Latitude'] != 'None')):
        df['geometry'] = df.apply(lambda x: Point(
            (float(x['Longitude']), float(x['Latitude']))), axis=1)
        shapefile = geopandas.read_file(r'shapefiles\boundary_ncr.shp')
        crs = {'init': 'epsg:4326'}
        df = geopandas.GeoDataFrame(df, crs=crs, geometry='geometry')
        df_gpd = geopandas.sjoin(df, shapefile, how='left', op='within')
        df_gpd.drop(['index_right', 'geometry'], axis=1, inplace=True)
        df_gpd.rename(columns={'NAME_2': 'City'}, inplace=True)
        df_gpd = df_gpd[['Date', 'Time', 'City', 'Location', 'Latitude', 'Longitude', 'Direction',
                         'Type', 'Lanes_Blocked', 'Involved', 'Tweet', 'Source']]
        return df_gpd

    def convert_database_to_csv(self, csv_out_path):
        """Convert entire SQL incidents database to a CSV file"""
        df = pd.read_sql_query(f'SELECT * FROM {self.SQL_TABLE}', self.conn)
        df.to_csv(csv_out_path, index=False)

    def insert(self, row):
        """INSERT SQL command.
        Input sql_cmd_values is tuple containing all variables from Tweet2Map.
        It must be in the same order as the columns of the database."""

        tweet_date = row[1]['Date']
        tweet_time = row[1]['Time']
        tweet_city = row[1]['City']
        tweet_location = row[1]['Location']
        tweet_latitude = row[1]['Latitude']
        tweet_longitude = row[1]['Longitude']
        tweet_high_accuracy = row[1]['High_Accuracy']
        tweet_direction = row[1]['Direction']
        tweet_type = row[1]['Type']
        tweet_lanes = row[1]['Lanes_Blocked']
        tweet_involved = row[1]['Involved']
        tweet_text = row[1]['Tweet']
        tweet_id = row[1]['Source']

        sql_cmd_vals = (tweet_date, tweet_time, tweet_city, tweet_location, tweet_latitude, tweet_longitude,
                        tweet_high_accuracy, tweet_direction, tweet_type, tweet_lanes, tweet_involved,
                        tweet_text, tweet_id)

        sql_placeholder = '?, ' * self.num_columns
        sql_placeholder = sql_placeholder.rstrip(', ')
        sql_cmd = "INSERT INTO {} VALUES ({})".format(self.SQL_TABLE, sql_placeholder)

        self.c.execute(sql_cmd, sql_cmd_vals)
        self.conn.commit()

        return


class LocationDatabaseSQL:
    """Object based management of location database"""

    SQL_TABLE = 'LOCATIONS'

    def __init__(self, sql_database_file=None, verbose=False):

        # If empty, create default database
        if not os.path.exists(sql_database_file):
            default_new_database = os.path.join('data', 'locations.sqlite')
            if not os.path.exists('data'):
                # Make folder if not existing
                os.mkdir('data')
            if verbose:
                print(f'WARNING: SQL database not detected. Creating new database: {default_new_database}')
            self.sql_database_file = sql_database_file = default_new_database
            conn = sqlite3.connect(self.sql_database_file)
            cols = ['Location', 'Coordinates', 'High_Accuracy']
            df = pd.DataFrame(columns=cols)
            df.to_sql(name=self.SQL_TABLE, con=conn)
            conn.close()

        self.sql_database_file = sql_database_file
        self.conn = sqlite3.connect(self.sql_database_file)
        self.c = self.conn.cursor()
        self.num_columns = self.conn.execute(
            'SELECT * FROM {} LIMIT 1'.format(self.SQL_TABLE))
        self.num_columns = len([col[0] for col in self.num_columns.description])
        self.columns = self.conn.execute('SELECT * FROM {} LIMIT 1'.format(self.SQL_TABLE))
        self.columns = [col[0] for col in self.columns.description]
        self.row_count = len(pd.read_sql_query(f'SELECT * FROM {self.SQL_TABLE}', self.conn))

    def search_matching_location(self, location):
        """Search location and prints a list of results. Returns select location and coordinate in a tuple."""

        # Read database
        df = pd.read_sql_query(f'SELECT * FROM LOCATIONS WHERE Location LIKE "%{location}%"', self.conn)
        
        # Display information
        for item in df.iterrows():
            print(item[0], item[1]['Location'], item[1]['Coordinates'])

        # Get user input to select location
        user_selection = input('Select location by index:')
        if user_selection == 'BREAK':
            return 'BREAK'
        # location = df.iloc[user_selection]['Location']
        coords = df.iloc[int(user_selection)]['Coordinates']
        bool_high_accuracy = df.iloc[int(user_selection)]['High_Accuracy']

        return (location, coords, bool_high_accuracy)

    def get_location_dictionary(self):
        """Get dictionary object where key is location and value is coordinate"""
        df = pd.read_sql_query(f'SELECT * FROM LOCATIONS', self.conn)
        location_dict = dict(zip(df['Location'], df['Coordinates']))
        location_accuracy_dict = dict(zip(df['Location'], df['High_Accuracy']))
        return location_dict, location_accuracy_dict

    def insert(self, location, coordinates, high_accuracy):
        """INSERT SQL command.
        Input sql_cmd_values is tuple containing all variables from Tweet2Map.
        It must be in the same order as the columns of the database."""

        sql_cmd_vals = (location, coordinates, high_accuracy)

        sql_placeholder = '?, ' * self.num_columns
        sql_placeholder = sql_placeholder.rstrip(', ')
        sql_cmd = "INSERT INTO {} VALUES ({})".format(self.SQL_TABLE, sql_placeholder)

        self.c.execute(sql_cmd, sql_cmd_vals)
        self.conn.commit()
        
    def close_connection(self):
        """Close SQL database connection"""
        self.c.close()
        self.conn.close()
