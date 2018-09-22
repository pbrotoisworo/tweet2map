# MMDA Tweet2Map
MMDA Tweet2Map is a python script that converts MMDA tweets into a usable database for traffic accident research in Metro Manila. Please take note that you need your own unique Twitter API code in order to use this script. This script uses the **tweepy library** in order to connect with the Twitter API.

For more information regarding this script please visit the project page on my blog:

https://panjib.wixsite.com/blog/mmdatweet2map

MMDA Twitter Page here:

https://twitter.com/MMDA

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

