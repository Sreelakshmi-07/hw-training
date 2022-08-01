import requests
from parsel import Selector
import json
import pymongo


client = pymongo.MongoClient("localhost",27017)
db = client.olxhouses

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page='



fieldname=['property_name','property_id','breadcrumbs','price','img','description','seller_name','location','property_type','bathroom','bedrooms']


def crawl(url):
  
        for page in range(1, 2):
            next_page = url + str(page)
            print(next_page)
            pages = requests.get(next_page, headers=headers).text
            selector = Selector(text=pages)

            allowed_domain = 'http://www.olx.in'
            for houses in selector.xpath("//ul[@data-aut-id='itemsList']/li"):

                link = houses.xpath('a/@href').extract_first()

                if link is not None:

                    item_response = requests.get(url=allowed_domain + link,
                                                 headers=headers).text
                    item_data = Selector(text=item_response)

                    response(item_data)


def response(item_data):


        list1 = ' '.join(map(str,
                        item_data.xpath("//span[@data-aut-id='itemPrice']/text()"
                                        ).getall()))

        convert_list = list1.split(' ')
        for price_dict in range(len(convert_list)):

                price_dict = {'amount': convert_list[0]}
        price_dict = {
                'amount': convert_list[-1],
                'currency': convert_list[0]
                }

        bathroom = item_data.xpath("//div/span[@data-aut-id='value_bathrooms']/text()"
                                                    ).get()
        if bathroom is None:
                bathrooms = int(bathroom or 0)
        else:
                bathroom_string = bathroom.split("+")
                bathroom_list = [val for val in bathroom_string if val.isdigit()]
                bathrooms = ''.join(bathroom_list)


        bedroom = item_data.xpath("//div/span[@data-aut-id='value_rooms']/text()"
                                                    ).get() 
        if bedroom is None:
                bedrooms = int(bedroom or 0)
        else:
                bedroom_string = bedroom.split("+")
                bedroom_list = [val for val in bedroom_string if val.isdigit()]
                bedrooms = ''.join(bedroom_list)
                
        



        properties = {
                        'property_name': item_data.xpath("//h1[@data-aut-id='itemTitle']/text()"
                                                         ).get(),
                        'property_id': ' '.join(map(str,
                                                    item_data.xpath("//div/strong[contains(text(),'AD ID')]/text()"
                                                                    ).re(r"\d+"))),
                        'breadcrumbs': item_data.xpath("//div[@data-aut-id='breadcrumb']/div/ol/li/a/text()"
                                                       ).getall(),
                        'price': price_dict,
                        'img': item_data.xpath("//figure/img[@class='_39P4_']/@src"
                                               ).get(),
                        'description': item_data.xpath("//div[@data-aut-id='itemDescriptionContent']/p/text()"
                                                       ).get(),
                        'seller_name': item_data.xpath("//div[@data-aut-id='profileCard']/div/a/div/text()"
                                                       ).get(),
                        'location': item_data.xpath("//div[@data-aut-id='itemLocation']/div/span/text()"
                                                    ).get(),
                        'property_type': item_data.xpath("//div/span[@data-aut-id='value_type']/text()"
                                                         ).get(),
                        'bathroom': int(bathrooms),
                        'bedrooms': int(bedrooms),
        }
        # print(properties)

        db.houseproperties.insert_one(properties)
        

crawl(url)

