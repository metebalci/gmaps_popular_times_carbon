This software is based on [gmaps_popular_times_scraper](https://github.com/philshem/gmaps_popular_times_scraper). I did not fork it because this is going to be a heavily modified version and might turn into something very different.

# Description

This software looks at a csv file in the following format (first row is headers):

```
url,name
```

The url is expected to be a link to google maps location with popular times information (usually businesses or metro stops etc.).

Then it fetches this url, renders (using Chrome/ChromeDriver), parses the popular times information and sends this information to a carbon instance. It then can be used with Grafana etc.

# Install

- create a virtualenv

- pip3 install -r requirements.txt

- Modify these lines in the code `config.py` to point to your path of Chrome and chromedriver.

```
CHROME_BINARY_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROMEDRIVER_BINARY_LOCATION = '/usr/local/bin/chromedriver'
```

Chromedriver downloads are [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure you use the version that matches your Chrome version.
