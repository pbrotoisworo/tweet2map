# MMDA Tweet2Map
MMDA Tweet2Map is a python script that mines MMDA Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **tweepy library** in order to connect with the Twitter API. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map).

I'm open to suggestions and comments! This is my first major coding project since I started self-learning Python.

# **Upcoming:**
- Streamline main script by utilizing more classes and functions
- Fix parsing logic regarding incidents involving rallyists
- Code to automatically push database updates to the project's [Kaggle page](https://www.kaggle.com/esparko/mmda-traffic-incident-data)
- Spatial joins through FOSS tools instead of ArcGIS Software

# Table of Contents
1. [Important: ArcPy Package](#arcpy)
2. [Code Structure and Configuration](#structure)
3. [Usage](#Usage)
4. [Changelog](#changelog)

## ArcPy Package <a name="arcpy"></a>
ArcPy is used in this script but is only required if you want to add the 'City' column to your data. The file uses the [ArcPy package](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v000000v7000000.htm), which comes with ArcGIS, to integrate and automate geospatial analysis. This Python package comes with ArcGIS and is not available through `pip install` options. The script is written in Python 3 but `arcpy_Spatial_Join_City.py` was written in a Python 2 environment since I'm still using ArcMap 10.6.

## Code Structure and Configuration <a name="structure"></a>
The main script `Tweet2Map.py` runs in **Python 3.6** and above while the Spatial Join runs in **Python 2** through the ArcGIS Python package. Additional functions, classes, configuration, and ArcPy code is stored in the modules folder. The script can combine separate Python interpreters by executing them through the `run_program.bat` file.

You can configure settings for the script such as Tweepy API tokens and whether or not you want the ArcPy module to run. This can be done in the `config.ini` file.

The parameters are:

- `arcpy_module_installed`: User can set this. If you don't have the arcpy module installed set this to False and it will prevent the script from running.
- `parser_error`: **DO NOT CHANGE.** Automatically set to True if there was an error in the main script. Prevents ArcPy script file from executing. It outputs that an error is detected then closes the script.
- `arcpy_run`: **DO NOT CHANGE.** Automatically set to True if there is another condition where the ArcPy script doesn't need to run. Does not output error message.

In the Tweepy section, input your Twitter API codes which the script will use to connect to the Twitter API.

## Usage <a name="Usage"></a>
Use the `run_program.bat` file to run the full code. You can execute the code using different Python interepreters by typing in the full link of the python.exe file. Afterwards, you put in the full link of the .py file you want to run. Use the following example below which is the placeholder information currently in the .bat file:
```
@echo off
"C:\ProgramData\Anaconda3\python.exe" "C:\Users\Panji\Documents\Python Scripts\MMDA Tweet2Map\Tweet2Map.py"
"C:\Python27\ArcGIS10.6\python.exe" "C:\Users\Panji\Documents\Python Scripts\MMDA Tweet2Map\arcpy_Spatial_Join_City.py"

```
In this case, I'm typing in the full path of the Python 3 interpreter I use from the Anaconda distribution for my Python 3 interpreter then I put in the Tweet2Map path. The following line is the full path of the Python 2 interpreter then the ArcPy script I use to run the spatial join.

## Changelog <a name="changelog"></a>

0.9 (TBA)
- Fixed parsing logic regarding incidents in Quezon City Elliptical Road
- Added a `config.ini` file where you can put in the Tweepy API code and configure some settings
- Added code to prevent the ArcPy script from executing if there is an error in the first .py file
- Updated timezone of extracted tweets from GMT+0 to GMT+8 to match Manila local time

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
