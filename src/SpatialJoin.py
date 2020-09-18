import pandas as pd
import geopandas as gpd


def spatial_join(df_input, shapefile):

    # Load shapefile
    shapefile = gpd.read_file(shapefile)
    shapefile.drop(['GID_0', 'GID_1', 'NL_NAME_1', 'GID_2', 'VARNAME_2', 'NL_NAME_2', 'TYPE_2', 'NAME_0',
                    'NAME_1', 'ENGTYPE_2', 'CC_2', 'HASC_2'], axis=1, inplace=True)
    # shapefile.crs = {'init': 'epsg:4326'}
    shapefile.crs = 'epsg:4326'

    # Load Excel file

    df = gpd.GeoDataFrame(
        df_input, geometry=gpd.points_from_xy(df_input['Longitude'], df_input['Latitude']))
    # df.crs = {'init': 'epsg:4326'}
    df.crs = 'epsg:4326'

    # Spatial Join
    df = gpd.sjoin(df, shapefile, how='left', op='within')
    df.drop(['index_right', 'geometry'], axis=1, inplace=True)
    df.rename(columns={'NAME_2': 'City'}, inplace=True)
    df = df[['Date', 'Time', 'City', 'Location', 'High_Accuracy', 'Latitude', 'Longitude', 'Direction',
             'Type', 'Lanes_Blocked', 'Involved', 'Tweet', 'Source']]

    return df
