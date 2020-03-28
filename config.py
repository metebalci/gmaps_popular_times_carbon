import os

# give time to download map tiles
SLEEP_SEC = 30.0

# csv output delimiter
DELIM = ','
HEADER_COLUMNS = ('place', 'url', 'scrape_time', 'day_of_week', 'hour_of_day', 'popularity_percent_normal', 'popularity_percent_current')

# path to chrome and chromedriver
CHROME_BINARY_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROMEDRIVER_BINARY_LOCATION = '/Users/mete/bin/chromedriver'

# keep an cache of the source htmls, with a timestamp in the filename
# if so, they should be cleaned out once in a while, since they are 1MB each
SAVE_HTML = True

CARBON_SERVER = 'localhost'
CARBON_PORT = '2003'
