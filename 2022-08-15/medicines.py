import requests
from parsel import Selector
import json



headers = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    "Sec-Fetch-Site": 'same-origin',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
}

url = ["https://costplusdrugs.com/medications/abacavirlamivudine-600mg_300mg-tablet/",
"https://costplusdrugs.com/medications/acetazolamide-250mg-tablet/",
"https://costplusdrugs.com/medications/Acyclovir-400mg-Tablet/",
"https://costplusdrugs.com/medications/albendazole-200mg-tablet/",
"https://costplusdrugs.com/medications/albuterol-90mcg-inhaler8_5g/",
"https://costplusdrugs.com/medications/albuterol-90mcg-inhaler18g/",
"https://costplusdrugs.com/medications/albuterol-90mcg-inhaler6_7g/",
"https://costplusdrugs.com/medications/AlbuterolSulfate-0_083-Nebulization%20Solution/",
"https://costplusdrugs.com/medications/alendronate-70mg-tablet4pack/",
	"https://costplusdrugs.com/medications/alfuzosinhcler-10mg-tablet/"
]

def crawl(url):

	for links in url:

		response = requests.get(links,headers = headers)
		
		selector = Selector(text = response.text)
		data = selector.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()
		datas = json.loads(data)
		print(datas.get('props').get('pageProps').keys())
		responses(datas)

def responses(datas):

	data_keys = datas.get('props').get('pageProps').get('medicationDetails')
	# print(data_keys)
	medicine_details = {
    'medicine_name': data_keys['name'],
    'price':data_keys['priceOption1'],
    'form' : data_keys['form'],
    'strength' : data_keys['strength'],

	}
	# print(medicine_details)
	# with open ("medicine_details.json",'a') as f:
	# 	f.write(json.dumps(medicine_details,indent=4))

crawl(url)