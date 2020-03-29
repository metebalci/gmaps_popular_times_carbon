This software is based on [gmaps_popular_times_scraper](https://github.com/philshem/gmaps_popular_times_scraper). I did not fork it because this is going to be a heavily modified version and might turn into something very different.

# Description

This software looks at the urls.csv file in the following format (first row is headers):

```
url,name
```

The url is expected to be a link to google maps location with popular times information (usually businesses or metro stops etc.). Click on the location, click share, and copy link.

Then it fetches this url, renders using Chrome/ChromeDriver, parses response to find the popular times information and sends this information to a graphite carbon instance. It then can be used with Grafana etc. The label of the data sent to carbon is popular_times.<name> where the <name> is in urls.csv.

It is possible to pass a single string as a command line argument, in this case only this url with that name is processed.

# Install

- pip3 install -r requirements.txt

- Modify these lines in the code `config.py` to point to your path of Chrome and chromedriver.

```
CHROME_BINARY_LOCATION = ''
CHROMEDRIVER_BINARY_LOCATION = ''
```
# About Popular Times

How Google calculates this is -naturally- not known in detail, but average time is said to be calculated considering some number of past weeks and live data is given relative to a peak value in average data. Both average and live are percents. It is difficult to compare the numbers between weeks since it is a relative measure (and it changes every week), but it probably gives a good estimation of a trend.
