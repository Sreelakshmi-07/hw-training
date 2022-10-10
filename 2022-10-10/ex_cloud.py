import cloudscraper
import requests
from parsel import Selector
import js2py
import time
# headers = {
#       'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
# }
scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'linux',
        'desktop': True},delay = 5 )
time.sleep(10)
print(scraper.get('https://www.yelp.com/').status_code)

url = scraper.get('https://www.yelp.com/').text
print(url)
selector = Selector(text=url)
name = selector.xpath("//a[class='link__09f24__nEC8H css-1sie4w0']/@href").extract()
print(name)
