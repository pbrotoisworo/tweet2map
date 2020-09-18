# Tweet2Map

**Author:** Panji Brotoisworo

**Contact: [panji.p.broto@gmail.com](mailto:panji.p.broto@gmail.com)**

Tweet2Map is a python script that mines Metro Manila Development Authority (MMDA) Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **Tweepy library** in order to connect with the Twitter API, **Geopandas** and **Shapely** for the Spatial Join, and uses **RegEx** for text parsing. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map). This project is in no way affiliated with the MMDA and is a personal project.

# Upcoming
- Spellchecker using the Peter Norvig algorithm to fix typos and wrong spelling of locations and other information
- Permutations to try different combinations of locations
  - Eg, if the script cannot find EDSA ORTIGAS MRT, it will try EDSA MRT ORTIGAS, and so on
- Natural Language Processing to replace RegEx (maybe)
  - Focus primarily on named entity recognition to extract data

# Getting Started

## Create Your Virtual Environment
It is recommended that you install a Python 3.8 virtual environment. Though I think a 3.6 environment may still work. Once the environment is installed, install the relevant packages by installing these libraries:

`tweepy pandas geopandas`

Run the `main.py` to initialize and create the config file.

## Input Twitter Tokens
Create a Twitter developer account and get your own Twitter API tokens [here](https://developer.twitter.com/en). Afterwards, you have 2 options of entering your API tokens into the Tweet2Map software. You can manually input the tokens into the `config.ini` file or you can input them via the CLI using these arguments:

- `-consumer_secret`
- `-consumer_key`
- `-access_token`
- `-access_secret`

## Downloading Tweets to Cache
Start downloading and caching tweets for later processing by running `main.py` without any arguments. This is designed to be run on a schedule automatically so you can just set a schedule to run it automatically come back when you area ready to process the tweets and add them to the database.

## Process The Tweet Data
Run the processing script by adding the `-p` argument as seen below:

`python main.py -p`

This will download the latest tweets and also load all the cached tweets. It will perform duplicate checks according to the tweet ID and will look in the newly downloaded tweets, cached tweets, and processed tweets in the incident database.

## Adding New Locations
You will inevitably run into new locations that are not in the database and you will encounter this prompt:

![New location](/doc/1_new_location.png)

You can check the database for an existing location. Often times there are many different names for the same location. In this case, there were no good matches so we go back to prompt by typing in "BREAK".

![New location](/doc/2_new_location.png)

So you can search for the location on Google Maps. In this case, "EDSA PINATUBO" resulted in a very precise location which we can add to the database.

![Searching on Google Maps](/doc/3_google_maps.png)

We get the location by right clicking the location and clicking "What's here?". This will reveal the coordinates which can be copy and pasted into the terminal.

![Extracting coords](/doc/4_google_maps.png)

We paste it into the prompt. Then type "Y" to confirm.

![Adding coords](/doc/5_adding_coords.png)

# Changelog

1.00 (September 19, 2020)
- Complete code rewrite for usability and readability
- Made script more modular. Moved functions to `src` folder
- Created automated script that will download and cache tweets for later processing
- Replaced CSV databases with SQLITE3 databases
- Added `High_Accuracy` column that is attached to the location to be able to filter accurate and inaccurate locations

0.95 (July 28, 2019)
- Replaced ArcMap spatial join workflow with a workflow that uses FOSS tools, Geopandas and Shapely
- Improved logging for more in-depth troubleshooting
- Compartmentalizing the code so that the main Tweet2Map.py script is easier to interpret
  - Transferred more parsing code to the TweetParse object
- Improved naming of .csv database files. The **spatial** tag on the filename means that null location data is removed. This was done in order to make it compatible with Geopandas and Shapely workflows. The **raw** includes null data but does not include City location data.
- Added option to manually fix the name if the code detects an unknown location. This is to prevent incorrect location names being fed into the location database
- Added option to set the location as invalid from the new location menu

0.9 (February 16, 2019)
- Fixed parsing logic regarding incidents involving rallyists
- Fixed parsing logic regarding incidents in Quezon City Elliptical Road
- Added a `config.ini` file where you can put in the Tweepy API code and configure some settings
- Added code to prevent the ArcPy script from executing if there is an error in the first .py file
- Updated timezone of extracted tweets from GMT+0 to GMT+8 to match Manila local time. The database still features a slight time discrepancy due to this. This will be fixed in a future update.
- Updated time parsing in the Tweetparse class to detect incorrect formats and fix them (EG, 10:18PM will be changed to 10:18 PM). The incorrect formats caused errors when converting the time data to a datetime object.

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
