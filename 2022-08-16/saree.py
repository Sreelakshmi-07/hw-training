import requests
from scrapy import Selector
import json
import csv
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
base_url = "https://www.saree.com/saree?p="


def crawl(base_url):
    for page in range(1, 9):
        next_page = base_url + str(page)
        # print(next_page)
        response = requests.get(next_page, headers=headers)
        # print(response.status_code)
        selector = Selector(text=response.text)
        for detailed_page in selector.xpath('//ol[@class="products list items product-items"]/li'):
            link = detailed_page.xpath(
                '//a[@class="product photo product-item-photo"]/@href').extract()
            link_len = len(link)
            for i in range(link_len):
                links = link[i]
                # print(links)

                responses(links)


def responses(links):

    link_response = requests.get(links)
    sel = Selector(text=link_response.text)
    saree_properties = {
        'product_name': sel.xpath('//span[@data-ui-id="page-title-wrapper"]/text()').extract_first(),
        'product_price': sel.xpath('//span[@class="price"]/text()').extract_first(),
        'product_code': sel.xpath('//td[@data-th="Product Code"]/text()').extract_first(),
        'product_color': sel.xpath('//td[@data-th="Color"]/text()').extract_first(),
        'product_work': sel.xpath('//td[@data-th="Work"]/text()').extract_first(),
        'product_blouse_fabric': sel.xpath('//td[@data-th="Blouse Fabric"]/text()').extract_first(),
        'product_blouse_type': sel.xpath('//td[@data-th="Blouse Type"]/text()').extract_first(),
        'product_dispatch': sel.xpath('//td[@data-th="Time To Dispatch"]/text()').extract_first()
    }
    # print(saree_properties)

    with open("sarees.json", 'a') as f:
        f.write(json.dumps(saree_properties, indent=4))
 


crawl(base_url)
