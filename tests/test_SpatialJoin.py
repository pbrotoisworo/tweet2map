import geopandas as gpd
import pandas as pd
from src.SpatialJoin import spatial_join

TESTS_DIR = os.path.dirname(__file__)
shp_path = os.path.join(TESTS_DIR, 'test_data', 'boundary_ncr.shp')
test_csv_path = os.path.join(TESTS_DIR, 'test_data', 'spatial_join_test.csv')

def test_spatial_join():
    
    df = pd.read_csv(test_csv_path)
    df_spatial = spatial_join(df, shp_path)
    message = f'Assertion of Spatial join failed. City column not detected. Detected columns: {df_spatial.columns}'
    assert 'City' in df_spatial.columns, message

def test_city_column_data():
    
    df = pd.read_csv(test_csv_path)
    df_spatial = spatial_join(df, shp_path)
    
    expected = ['Pasig City', 'Mandaluyong', 'Makati City']
    actual = list(df_spatial['City'])
    message = f'Test of City spatial join failed. Expected "City" column data: {expected}. Actual data: {actual}'
    assert expected == actual, message