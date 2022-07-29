import requests
from parsel import Selector
import json
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
url = 'https://www.olx.in/api/relevance/v2/search?category=1723&facet_limit=100&lang=en-IN&location=4058877&location_facet_limit=20&platform=web-desktop&size=40&page='
field_name = ['property name','property id','price','img','ratings','description','location','property type','bathroom','bedrooms']

def get(url):

    for page in range(1, 3):
        data = ''
        next_page = url + str(page)
        pages = requests.get(next_page, headers=headers).json()
        # print(pages)
        with open('datas_olx.json', 'w') as f:
            f.write(json.dumps(pages, indent=4))
        with open('datas_olx.json', 'r') as jf:
            for lines in jf.read():
                data += lines
            datas = json.loads(data)

        response(datas)


def response(datas):

    for properties in datas['data']:
        property_house = {
            'property name': properties['title'],
            'property id': properties['id'],
            'price': {properties['price']['value']['raw'], properties['price']['value']['currency']['pre']},
            'img': properties['images'][0]['url'],
            'description': properties['description'],
            'location': properties['locations_resolved']['SUBLOCALITY_LEVEL_1_name']+','
            + properties['locations_resolved']['ADMIN_LEVEL_3_name']+','
            + properties['locations_resolved']['ADMIN_LEVEL_1_name'],
            'property type': properties['parameters'][0]['value_name'],
            'bathroom': properties['parameters'][2]['value_name'],
            'bedrooms': properties['parameters'][1]['value_name']
        }
        print(property_house)
        with open("olxapis.csv", 'a') as cfile:
            writer = csv.DictWriter(cfile, fieldnames=field_name)
            writer.writeheader()
            writer.writerow(property_house)


get(url)
