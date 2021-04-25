
import json
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap, MarkerCluster

from src.streamlit.dataframe_filter import DatabaseFilter

def main():

    csv_file = 'data_mmda_traffic_spatial.csv'

    @st.cache
    def load_df(path):
        df = pd.read_csv(path)
        df = df.dropna()
        return df

    def load_shp(path):
        gdf = gpd.read_file(path)
        gdf.to_file('boundary.json', driver='GeoJSON')
        with open('boundary.json') as f:
            json_file = json.load(f)
        return json_file

    # Load data
    city_list = (
        'NONE',
        'Kalookan City',
        'Makati City',
        'Malabon',
        'Mandaluyong',
        'Manila',
        'Marikina',
        'Navotas',
        'Parañaque',
        'Pasay City',
        'Pasig City',
        'Quezon City',
        'San Juan',
        'Taguig',
        'Valenzuela'
    )
    type_list = (
        'NONE',
        'Vehicular Accident',
        'Stalled Vehicle',
        'Multiple Collision',
        'Hit and Run'
    )

    #########################
    # START PAGE STRUCTURE HERE
    #########################

    # Page title
    st.title('Map Viewer')
    
    st.header('Filter Data')
    max_tail = st.number_input('Number of latest data to show:', value=1000)
    col1, col2 = st.beta_columns(2)
    with col1:
        type_filter = st.multiselect('Type of Incident', type_list)
    with col2:
        city_filter = st.multiselect('City of Incident', city_list)

    df_filter = DatabaseFilter(load_df(csv_file), type_filter, city_filter)
    
    # Load markers
    mc = MarkerCluster(name='Incidents')
    metro_coords = (14.599574, 121.059929)
    m = folium.Map(
        location=metro_coords,
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    df = df_filter.filter_data()
    df = df.tail(max_tail)  # Only get last 1000 pieces of data
    mc = MarkerCluster(name='Incidents')
    
    st.header('Data')
    st.text(f'Showing {len(df)} incidents')
    st.dataframe(df)

    
    # Populate map
    for item in df.iterrows():
        
        source = item[1]['Source']
        text = item[1]['Tweet']
        timestamp = item[1]['Date']
        embed = """
        <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
        </head>
        <div>
            <h3>Tweet:</h3>
            <blockquote class="twitter-tweet tw-align-center"><p lang="en" dir="ltr"> {} </a></p>&mdash; Official MMDA (@MMDA)<a href="{}"> {}</a></blockquote>
            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        """.format(text, source, timestamp)
        
        # Generate content for markers
        iframe = folium.IFrame(
            embed,
            width=500,
            height=280
        )
        
        # Put content in popup for markers
        popup = folium.Popup(iframe)
        mc.add_child(folium.Marker(location=[item[1]['Latitude'], item[1]['Longitude']],
                                    popup=popup,
                                    clustered_marker=True)).add_to(m)
    
    
    # Visualize webmap
    folium_static(m)
