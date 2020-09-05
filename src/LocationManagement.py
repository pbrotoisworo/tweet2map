import pandas as pd
import sqlite3
import os


class LocationDatabaseSQL:
    """Object based management of location database"""

    SQL_TABLE = 'LOCATIONS'

    def __init__(self, sql_database_file=None, verbose=False):

        # If empty, create default database
        if not os.path.exists(sql_database_file):
            default_new_database = r'data\locations.sql'
            if verbose:
                print(f'WARNING: SQL database not detected. Creating new database: {default_new_database}')
            self.sql_database_file = sql_database_file = default_new_database
            conn = sqlite3.connect(self.sql_database_file)
            cols = ['Location', 'Coordinates']
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
        
        # # Extract information
        # index = []
        # loc = []
        # loc_coords = []
        # for item in df.iterrows():
        #     index.append(item[0])
        #     loc.append(item[1]['Location'])
        #     loc_coords.append(item[1]['Coordinates'])
        # results = list(zip(index, loc, loc_coords))

        # Get user input to select location
        user_selection = int(input('Select location by index:'))
        location = df.iloc[user_selection]['Location']
        coords = df.iloc[user_selection]['Coordinates']

        return (location, coords)

    def get_location_dictionary(self):
        """Get dictionary object where key is location and value is coordinate"""
        df = pd.read_sql_query(f'SELECT * FROM LOCATIONS', self.conn)
        location_dict = dict(zip(df['Location'], df['Coordinates']))
        return location_dict
