import requests
from parsel import Selector
import json
import csv

url = 'https://www.nykaa.com/makeup/face/face-primer/c/233'
headers = {
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

faceprimers = []
field_name = ['main title','product title','listing price','sale price','ratings','total ratings','image']

def get(url):

	nykaa_url = requests.get(url, headers = headers).text
	selector  = Selector(text=nykaa_url)
	for primers in selector.xpath("//div[@class='css-d5z3ro']"):

		main_title = primers.xpath("//div[@id='title']/h1/text()").extract_first()
		link = primers.xpath("a/@href").extract_first()
		domain = 'https://www.nykaa.com'
		link_response = requests.get(url = domain+link,headers = headers).text
		link_selector = Selector(text = link_response)
		response(link_selector,main_title)

def response(link_selector,main_title):

	faceprimers.append({
		'main title':main_title,
		'product title' : link_selector.xpath("//h1[@class='css-1gc4x7i']/text()").extract_first(),
		'listing price' : link_selector.xpath("//span[@class='css-u05rr']/span/text()").extract_first(),
		'sale price' : link_selector.xpath("//span[@class='css-1jczs19']/text()").extract_first(),
		'ratings' :(
		 	link_selector.xpath("//div[@class='css-m6n3ou']/text()").extract_first(),
			link_selector.xpath("//div[@class='css-m6n3ou']/span/text()").extract_first()
			),
		'total ratings' : link_selector.xpath("//div[@class='css-1hvvm95']/text()").extract_first(),
		'image' : link_selector.xpath("//div[@class='css-cqq5od']/div/img/@src").extract_first()
		})

	filename = f"nykaa_face_primers.json"
	with open(filename,"w") as f:
		f.write(json.dumps(faceprimers,indent = 4))


	file_name = f"nykaa_faceprimers.csv"
	with open(file_name,"w") as cfile:
		writer = csv.DictWriter(cfile,fieldnames = field_name)
		writer.writeheader()
		writer.writerows(faceprimers)




get(url)