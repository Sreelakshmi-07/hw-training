import urllib.request
from urllib.parse import *
request_url = urllib.request.urlopen('https://www.techwithtim.net/')
print(request_url.read())
print("\n")
parse_url = urlparse('https://www.techwithtim.net/')
print(parse_url)