import requests
import json
from parsel import Selector

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page='

properties = []
for page in range(1, 2):
    next_page = url + str(page)
    pages = requests.get(next_page, headers=headers).text
    selector = Selector(text=pages)

    allowed_domain = 'http://www.olx.in'
    for houses in selector.xpath("//ul[@data-aut-id='itemsList']/li"):

        link = houses.xpath('a/@href').extract_first()

        if link is not None:
            
            item_response = requests.get(url=allowed_domain + link,
                    headers=headers).text
            item_data = Selector(text=item_response)
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

            properties.append({
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
                'property_type': item_data.xpath("//div[@data-aut-id='itemParams']/div/div/div/span[@data-aut-id='key_type']/following-sibling::span[@data-aut-id='value_type']/text()"
                        ).get(),
                'bathroom': item_data.xpath("//div[@data-aut-id='itemParams']/div/div/div/span[@data-aut-id='key_rooms']/following-sibling::span[@data-aut-id='value_rooms']/text()"
                        ).get(),
                'bedrooms': item_data.xpath("//div[@data-aut-id='itemParams']/div/div/div/span[@data-aut-id='key_bathrooms']/following-sibling::span[@data-aut-id='value_bathrooms']/text()"
                        ).get(),
                })
        print(properties)

        # filename = f"olx_example.json"
        # with open(filename, "w") as f:
        #     f.write(json.dumps(properties, indent=4))
