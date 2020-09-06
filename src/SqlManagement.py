import sqlite3
import pandas as pd
import geopandas
import os
from shapely.geometry import Point


class Tweet2MapDatabaseSQL:
    """Object based management of SQL Database"""

    SQL_TABLE = 'INCIDENTS'

    def __init__(self, sql_database_file=None, verbose=False):

        self.sql_database_file = sql_database_file

        # If empty, create default database
        if not os.path.exists(sql_database_file):
            default_new_database = r'data\data.sql'
            if verbose:
                print(f'WARNING: SQL database not detected. Creating new database: {default_new_database}')
            self.sql_database_file = sql_database_file = default_new_database
            conn = sqlite3.connect(self.sql_database_file)
            cols = ['Date', 'Time', 'City', 'Location', 'Latitude' ,'Longitude', 'Direction',
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

    def load_latest_tweets(self):
        df = pd.read_sql_query(
            "select Source from {} WHERE Date <= date('now') AND Date >=  date('now', '-2 day')".format(self.SQL_TABLE), self.conn)
        latest_values = list(df.values.flatten())
        return latest_values

    def get_newest_tweet_ids(self, count=200):
        """Gets the last n Tweets to prevent duplicates when processing new Tweepy data"""

        # Get original tweets from existing database
        df = pd.read_sql_query(f'SELECT * FROM {self.SQL_TABLE} ORDER BY date(Date) DESC LIMIT {count}', self.conn)
        id_list = list(df['Source'])
        
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
        tweet_direction = row[1]['Direction']
        tweet_type = row[1]['Type']
        tweet_lanes = row[1]['Lanes_Blocked']
        tweet_involved = row[1]['Involved']
        tweet_text = row[1]['Tweet']
        tweet_id = row[1]['Source']

        sql_cmd_vals = (tweet_date, tweet_time, tweet_city, tweet_location, tweet_latitude, tweet_longitude,
                        tweet_direction, tweet_type, tweet_lanes, tweet_involved, tweet_text, tweet_id)

        # sql_cmd_vals = (row_dict['Date'], row_dict['Time'], row_dict['City'], row_dict['Location'],
        #                 row_dict['Latitude'], row_dict['Longitude'], row_dict['Direction'],
        #                 row_dict['Type'], row_dict['Lanes_Blocked'], row_dict['Involved'], row_dict['Tweet'],
        #                 row_dict['Source'])

        sql_placeholder = '?, ' * self.num_columns
        sql_placeholder = sql_placeholder.rstrip(', ')
        sql_cmd = "INSERT INTO {} VALUES ({})".format(self.SQL_TABLE, sql_placeholder)

        self.c.execute(sql_cmd, sql_cmd_vals)
        self.conn.commit()

        return
