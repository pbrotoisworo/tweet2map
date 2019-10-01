# MMDA Tweet2Map

**Author:** Panji Brotoisworo

**Contact: [panji.p.broto@gmail.com](mailto:panji.p.broto@gmail.com)**

MMDA Tweet2Map is a python script that mines MMDA Tweets ([@mmda](https://twitter.com/MMDA)) into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **Tweepy library** in order to connect with the Twitter API, **Geopandas** and **Shapely** for the Spatial Join, and uses **RegEx** for text parsing. For more information regarding this script please visit the project page on my [blog](https://panjib.wixsite.com/blog/mmdatweet2map).

I'm open to suggestions and comments! This is my first major coding project since I started self-learning Python.

# **Upcoming:**
- Tweet2Map streaming version: a version where the script will continuously run and check the mmda page twice a day. The main Tweet2Map script will have a section to accomodate this streaming information. This is the main goal of this script.
- Spellchecker using the Peter Norvig algorithm to fix typos and wrong spelling of locations and other information
- Permutations to try different combinations of locations
  - Eg, if the script cannot find EDSA ORTIGAS MRT, it will try EDSA MRT ORTIGAS, and so on
- Natural Language Processing to replace RegEx (maybe)
  - Focus primarily on named entity recognition to extract data

# Table of Contents
1. [Code Structure and Configuration](#structure)
2. [Usage](#Usage)
3. [Changelog](#changelog)

## Code Structure and Configuration <a name="structure"></a>
The main script `Tweet2Map.py` runs in **Python 3.6**. Additional functions, classes, configuration, and ArcPy code is stored in the modules folder. The script can combine separate Python interpreters by executing them through the `run_program.bat` file.

You can configure settings for the script such as Tweepy API tokens and database locations. This can be done in the `config.ini` file.
In the Tweepy section, input your Twitter API codes which the script will use to connect to the Twitter API.

## Usage <a name="Usage"></a>
Use the `run_program.bat` file to run the full code. You can execute the code using different Python interepreters by typing in the full link of the python.exe file. Afterwards, you put in the full link of the .py file you want to run. Use the following example below which is the placeholder information currently in the .bat file:
```
@echo off
call activate tweet2map
python "C:\Users\Panji\Documents\Python Scripts\MMDA Tweet2Map\Tweet2Map.py"

```
In this case, I'm activating the tweet2map virtual environment, type **python** to open the python interpreter in the virtual environment, then I put in the Tweet2Map path.

Now let's get to running the script and adding new locations. Here is my workflow for running the script and adding new locations.

![1](https://i.imgur.com/R5p4TpA.png)

When you run the code you will inevitably run into new locations that need to be added to the database. Choose option 1 or 2 by typing them into the input. In this case I chose option 2 just to check if I can use an existing location's coordinate information and paste it into this new location. There are a lot of different ways to refer to the same location so this is a way to save time.

Take note that the search function only searches using exact string matches. So it is better to search for locations using one word. The code can accept upper-string or lower-string search entries since everything is converted to upper-case. In this case I chose to search using the term "lacson".

![2](https://i.imgur.com/QWxDoMb.png)

Here are all the existing locations in the location database that feature the Lacson string. If there was a matching location, you can simply select by typing the index number. For example, if I wanted to use the latitude/longitude information of ESPANA LACSON for my new location then I type in **649**. Then I confirm in the next input by pressing Y.

In this case, there are no matching locations. So I type "RESET" without the quotes in order to bring me back to the option page. Then I choose 1. At this point, use your favorite location software to find this new location. I like to use Google maps to look up coordinate information on the internet. I type in Lacson Loyola which gives me the details below.

![3](https://i.imgur.com/kpYNZRH.png)

That looks about right. So I get the coordinate information by right clicking and clicking "What's here?" in order to give me the coordinate information. I click on the latitude/longitude information that pops up in the bottom of the screen. Then a text version that is easy to copy and paste will pop up on the left. I like to copy and paste that into the Command Prompt window instead of manually typing in the latitude and longitude.

![4](https://i.imgur.com/TNnQwuP.png)

Just confirm with Y and the script will continue processing the other tweets.

## Changelog <a name="changelog"></a>

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
