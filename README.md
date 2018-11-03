# MMDA Tweet2Map
MMDA Tweet2Map is a python script that converts MMDA Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the [tweepy library](http://www.tweepy.org/) in order to connect with the Twitter API. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map).

I'm open to suggestions and comments! This is my first major coding project since I started self-learning Python.

### ArcPy Package Information
The file uses the [ArcPy package](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v000000v7000000.htm), which comes with ArcGIS, to integrate and automate geospatial analysis. This Python package comes with ArcGIS and is not available through `pip install` options. ArcPy is used in this script but it is **not required**.

The ArcPy package allows you to add the 'City' column to the data through a Spatial Join. The script is written in Python 3 but `arcpy_Spatial_Join_City.py` was written in a Python 2 environment since I'm still using ArcMap 10.6.

### Usage

- Run script and let it automatically parse Twitter data
- Selecting options is done using by inputting the numbers associated with the action you want to do then follow the instructions on how to add the new location to the database

![Choicse for entering a new location](https://static.wixstatic.com/media/e7dfa2_d819bed373b14983a4612468f5169c0a~mv2.png/v1/fill/w_751,h_435,al_c,q_80,usm_0.66_1.00_0.01/e7dfa2_d819bed373b14983a4612468f5169c0a~mv2.webp)

# **Upcoming:**
- Fix some bugs with location and direction parsing
- Spell checker and auto-correct for location strings
  - Possible full automation of the script if auto-correct is accurate
- Streamline main script by utilizing more classes and functions
- ArcPy functions to automate heatmap calculations

# **Changelog:**

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
