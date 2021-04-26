import numpy as np
import pandas as pd
import streamlit as st

def main():
    
    csv_file = r'data/data.csv'
    @st.cache(allow_output_mutation=True)
    def load_df(path):
        df = pd.read_csv(path)
        df = df.dropna()
        return df
    
    df = load_df(csv_file)
    # Cast appropriate dtypes to columns
    df['Timestamp'] = df['Date'] + ' ' + df['Time']
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['High_Accuracy'] = df['High_Accuracy'].astype(int)
    df.replace('None', np.nan, inplace=True)
    
    # Get time series of dates
    df_date = df.groupby(pd.Grouper(key='Timestamp', freq="D")).count()

    df_date = df_date.reset_index()
    df_date.drop(['Date','Time','Location','Latitude','Longitude','Direction','Lanes_Blocked',
                'Involved','Tweet','Type'], axis=1,inplace=True)
    df_date = df_date.rename(columns={'Source': 'y'})
    # df_date.to_csv('data\incidents_day.csv',index=False)

    #######################################
    # Create rolling average of Total Incidents
    #######################################
    
    df_date_rolling = df_date
    df_date_rolling.set_index('Timestamp',inplace=True)
    df_date_rolling['roll7_avg'] = df_date_rolling['y'].rolling(7).mean()
    df_date_rolling['roll7_std'] = df_date_rolling['y'].rolling(7).std()
    df_date.reset_index(inplace=True)
    df_date_rolling = df_date_rolling.set_index('Timestamp')

    # Plot
    st.header('Total Incidents')
    st.subheader('Rolling Weekly Average')
    st.line_chart(df_date_rolling.drop(['y', 'High_Accuracy', 'City'], axis=1))
    
    #######################################
    # Total Incidents Compared to Incident Participants
    #######################################
    
    df_type = df
    df_type = df_type.dropna()

    def subset_mechanical_bus(row):
        if ('BUS' in row['Involved']) and ('MECHANICAL' in row['Type']):
            return True

    def subset_mechanical_truck(row):
        if ('TRUCK' in row['Involved']) and ('MECHANICAL' in row['Type']):
            return True
        
    def subset_mechanical_car(row):
        if (('CAR' in row['Involved']) or ('SUV' in row['Type'])) and ('MECHANICAL' in row['Type']):
            return True
        
    def subset_mechanical_public(row):
        if (('PUJ' in row['Involved']) or ('UV' in row['Type'])) and ('MECHANICAL' in row['Type']):
            return True

    # Subset
    df_type['type_bus'] = df_type.apply(lambda row: subset_mechanical_bus(row),axis=1)
    df_type['type_truck'] = df_type.apply(lambda row: subset_mechanical_truck(row),axis=1)
    df_type['type_public'] = df_type.apply(lambda row: subset_mechanical_public(row),axis=1)
    df_type['type_car'] = df_type.apply(lambda row: subset_mechanical_car(row),axis=1)

    # Create dataframe and plot
    df_type_participant = df_type[['Timestamp','type_bus','type_truck','type_public','type_car']]
    
    st.subheader('Rolling Weekly Average By Participant')
    st.line_chart(df_type_participant.groupby(pd.Grouper(key='Timestamp', freq="W")).sum().rolling(7).mean())
    
    #######################################
    # Plot by direction
    #######################################
    
    def subset_by_direction(df, direction):
        df_subset = df.dropna(subset=['Direction'])
        df_subset = df_subset[df_subset['Direction'].str.contains(direction)]
        df_subset = df_subset['Timestamp'].dt.hour.value_counts()
        df_subset = df_subset.rename_axis('Hour').reset_index(name=f'Amount_{direction}')
        df_subset = df_subset.sort_values(by='Hour')
        df_subset['Hour'] = df_subset['Hour'].astype(int)
        df_subset = df_subset.reset_index(drop=True)
        df_subset.set_index('Hour',inplace=True)
        return df_subset

    df_sb = subset_by_direction(df, 'SB')
    df_nb = subset_by_direction(df, 'NB')
    df_eb = subset_by_direction(df, 'EB')
    df_wb = subset_by_direction(df, 'WB')

    df_direction = pd.concat([df_nb, df_sb, df_eb, df_wb],axis=1)

    # Average amount of incidents per direction
    df_direction['Amount_NB'] = df_direction['Amount_NB'] / len(df_direction)
    df_direction['Amount_SB'] = df_direction['Amount_SB'] / len(df_direction)
    df_direction['Amount_EB'] = df_direction['Amount_EB'] / len(df_direction)
    df_direction['Amount_WB'] = df_direction['Amount_WB'] / len(df_direction)

    # Plot
    st.subheader('Incidents by Lane Direction')
    st.line_chart(df_direction)