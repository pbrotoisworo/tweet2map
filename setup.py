from setuptools import setup, find_packages

setup(
    name='tweet2map',
    author='Panji P. Brotoisworo',
    url='https://github.com/pbrotoisworo/tweet2map',
    version=1.0,
    packages=[
        'src',
        'tests',
        r'tests.test_data',
        'shapefiles'
    ],
    include_package_data=True,
    package_data={
        r'tests': ['*'],
        r'tests.test_data': ['*'],
        r'shapefiles': ['*']
    },
    install_requires=[
		'shapely==1.7.1',
		'geos',
		'descartes',
        'tweepy',
		'pandas',
        'geopandas',
        'rtree',
        'streamlit',
        'streamlit-folium'
    ]
)