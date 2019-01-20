# MMDA Tweet2Map
MMDA Tweet2Map is a python script that converts MMDA Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **tweepy library** in order to connect with the Twitter API. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map).


### ArcPy Package Information
`ArcPy` is used in this script but is only required if you want to add the 'City' column to your data. The file uses the [ArcPy package](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v000000v7000000.htm), which comes with ArcGIS, to integrate and automate geospatial analysis. This Python package comes with ArcGIS and is not available through `pip install` options. The script is written in Python 3 but `arcpy_Spatial_Join_City.py` was written in a Python 2 environment since I'm still using ArcMap 10.6.

I'm open to suggestions and comments! This is my first major coding project since I started self-learning Python.

# **Upcoming:**
- Fix some bugs with location and direction parsing
- Spell checker and auto-correct for location strings
  - Possible full automation of the script if auto-correct is accurate
- Streamline main script by utilizing more classes and functions
- Fix parsing logic regarding incidents involving rallyists

# **Changelog:**

0.9 (TBA)
- Fixed parsing logic regarding incidents in Quezon City Elliptical Road
- Added a `config.ini` file where you can put in the Tweepy API code and configure some settings
- Added code to prevent the ArcPy script from executing if there is an error in the first .py file

0.8 (October 23, 2018)
- Added City column through ArcPy package into script
- Added .bat script `run_program.bat` to execute scripts in one motion
- Fixed some bugs when the user would search the database
- Restructured some of the code
 - Removed nested while loops

0.7 (September 22, 2018)
- Fixed some bugs with the location parsing
- Added more words to the `location_string_clean()` function
- Added more locations to the database

0.6 (September 15, 2018)
- Created the `tweetParse` class to streamline parts of the code in `Tweet2Map.py`
- Some small bug fixes to take into account MMDA alerts for rallyists.

0.5
- Added options on what to do with new locations to streamline parsing
