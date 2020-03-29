This software is based on [gmaps_popular_times_scraper](https://github.com/philshem/gmaps_popular_times_scraper). I did not fork it because this is going to be a heavily modified version and might turn into something very different.

# Description

This software looks at the urls.csv file in the following format (first row is headers):

```
url,name
```

The url is expected to be a link to google maps location with popular times information (usually businesses or metro stops etc.). Click on the location, click share, and copy link.

Then it fetches this url, renders using Chrome/ChromeDriver, parses response to find the popular times information and sends this information to a graphite carbon instance. It then can be used with Grafana etc. The label of the data sent to carbon is popular_times.<name> where the <name> is in urls.csv.

# Install

- pip3 install -r requirements.txt

- Modify these lines in the code `config.py` to point to your path of Chrome and chromedriver.

```
CHROME_BINARY_LOCATION = ''
CHROMEDRIVER_BINARY_LOCATION = ''
```
