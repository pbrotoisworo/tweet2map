[![Build Status](https://travis-ci.com/pbrotoisworo/tweet2map.svg?branch=master)](https://travis-ci.com/pbrotoisworo/tweet2map)  [![codecov](https://codecov.io/gh/pbrotoisworo/tweet2map/branch/master/graph/badge.svg?token=U2F1H66DUB)](https://codecov.io/gh/pbrotoisworo/tweet2map) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Version](https://img.shields.io/badge/version-1.0-blue)

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
It is recommended that you install a Python 3.8 virtual environment. At minumum a 3.6 environment may still work. Once the environment is installed, install the relevant packages by installing these libraries:

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
