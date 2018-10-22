# MMDA Tweet2Map
MMDA Tweet2Map is a python script that converts MMDA Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **tweepy library** in order to connect with the Twitter API. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map).

The script is written in Python 3 but `arcpy_Spatial_Join_City.py` was written in a Python 2 environment since I'm still using ArcMap 10.6. The file uses the `ArcPy` library to integrate and automate geospatial analysis and that comes with ArcGIS.

I'm open to suggestions and comments! This is my first major coding project since I started self-learning Python.

# **Upcoming:**
- Fix some bugs with location and direction parsing
- Spell checker and auto-correct for location strings
  - Possible full automation of the script if auto-correct is accurate
- More locations in the database
- Streamline main script by utilizing more classes and functions

# **Changelog:**

0.7 (September 22, 2018)
- Fixed some bugs with the location parsing
- Added more words to the `location_string_clean()` function
- Added more locations to the database

0.6 (September 15, 2018)
- Created the `tweetParse` class to streamline parts of the code in `Tweet2Map.py`
- Some small bug fixes to take into account MMDA alerts for rallyists.

0.5
- Added options on what to do with new locations to streamline parsing
