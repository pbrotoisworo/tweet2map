# File for Streamlit data viewer
import pandas as pd
import numpy as np

class DatabaseFilter:
    
    def __init__(self, df, filter_type, filter_city, filter_date):
        
        self.df = df
        
        self.filter_type = filter_type if filter_type else None
        self.filter_city = filter_city if filter_city else None
        self.filter_datetime = filter_date if filter_date else None
        
    def filter_data(self):
        """
        Filter dataframe programmatically using SQL query
        """
        df_filtered = self.df
        
        # Filter by datetime
        # Build datetime query
        if self.filter_datetime:
            min_date = self.filter_datetime[0] if self.filter_datetime[0] else None
            max_date = self.filter_datetime[1] if self.filter_datetime[1] else None
            df_filtered = df_filtered[(df_filtered['Datetime'] > np.datetime64(min_date)) & (df_filtered['Datetime'] < np.datetime64(max_date))]
            
        
        # Build city query
        query_city = ''
        if self.filter_city:
            for city in self.filter_city:
                query_city += f'City == "{city.title()}" | '
            query_city = '(' + query_city.rstrip(' | ') + ')'
        
        # Build type query
        query_type = ''
        if self.filter_type:
            for type_ in self.filter_type:
                query_type += f'Type == "{type_.upper()}" | '
            query_type = '(' + query_type.rstrip(' | ') + ')'
            
        # Combine queries
        query = ''
        if query_city:
            query += f'{query_city} & '
        if query_type:
            query += f'{query_type} & '
        query = query.rstrip(' & ')
        
        # print('Query:', query, type(query))
        if query:
            df_filtered = df_filtered.query(query)
        
        return df_filtered
