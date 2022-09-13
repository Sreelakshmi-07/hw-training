import requests
from scrapy import Selector
import json
import logging

headers = {
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
start_url = [
    'https://www.olx.qa/en/properties/properties-for-rent/apartments-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/rooms-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/villas-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/chalet-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/land-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/commercial-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/multiple-units-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/buildings-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-rent/garage-for-rent/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/apartments-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/chalet-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/commercial-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/land-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/buildings-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/villas-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/garage-for-sale/',
    # 'https://www.olx.qa/en/properties/properties-for-sale/multiple-units-for-sale/',
]


def start_request(start_url):

    for url in start_url:

        response = requests.get(url, headers=headers)
        selector = Selector(text=response.text)
        allowed_domain = 'https://www.olx.qa'
        links = selector.xpath('//div[@class="ee2b0479"]/a/@href').extract()
        for href in links:
            link = requests.get(allowed_domain + href, headers=headers)
            sel = Selector(text=link.text)
            # ad_id = ' '.join(map(str, sel.xpath(
            #     "//div[text()[contains(.,'Ad id')]]/text()").re(r"\d+")))
            # api = 'https://www.olx.qa/api/listing/?external_id=' + str(120008296)
            # api_response = requests.get(url=api, headers=headers).json()
            # data = ''
            # # print(api_response.url)
            # with open('datas_olx.json', 'w') as f:
            #     f.write(json.dumps(api_response, indent=4))
            # with open('datas_olx.json', 'r') as jf:
            #     for lines in jf.read():
            #         data += lines
            #     datas = json.loads(data)

            # # print(datas)
            # page_dict = {'category_url': responses,
            #               'datas': datas}
            # responses(page_dict)

    next_page = selector.xpath(
        '(//div[@role="navigation"]//a)[last()]/@href').extract_first()
    if next_page:
        next_page_url = requests.get(
            url=allowed_domain + next_page, headers=headers)
        print(next_page_url.url)
        start_request(next_page_url)


# def responses(page_dict):

#     data = page_dict['datas']
#     # link = page_dict['link']
#     category_url = page_dict['category_url']
#     item = {
#         'id': data['externalID'],
#         # 'url': link.url,
#         'category': data['category'][0]['name'] + ','
#         + data['category'][1]['name'] + ','
#         + data['category'][2]['name'],
#         'title': data['title'],
#         'description': data['description'].split('AMENITIES')[0].encode('ascii', 'ignore').decode().replace("\n", ''),
#         'location': data['location'][2]['name'] + ',' + data['location'][1]['name'],
#         'price': '',
#         'amenities': data['description'].split('AMENITIES')[1].replace("\n",''),
#         'details' : {'Area (m²)':data['extraFields']['ft']},
#         'number_of_photos':'',
#         'published_at':''
#     }
    # print(item)


start_request(start_url)
