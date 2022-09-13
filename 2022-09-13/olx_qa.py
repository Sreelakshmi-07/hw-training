import scrapy
import json

from ..items import OlxQaItem
class Olxscrap(scrapy.Spider):

    # download_delay = 2
    name = 'olx'
    start_urls = [
        'https://www.olx.qa/en/properties/properties-for-rent/apartments-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/rooms-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/villas-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/chalet-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/land-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/commercial-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/multiple-units-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/buildings-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-rent/garage-for-rent/',
        'https://www.olx.qa/en/properties/properties-for-sale/apartments-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/chalet-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/commercial-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/land-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/buildings-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/villas-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/garage-for-sale/',
        'https://www.olx.qa/en/properties/properties-for-sale/multiple-units-for-sale/',
    ]
    headers = {
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url, headers=self.headers, callback=self.parse_link
            )

    def parse_link(self, response):

        url = response.url
        print(url)
        allowed_domain = 'https://www.olx.qa'
        links = response.xpath('//div[@class="ee2b0479"]/a/@href').extract()
        for href in links:
            link = href
            yield scrapy.Request(
                url=allowed_domain + link, headers=self.headers, callback=self.parse, cb_kwargs={'category_url': url}
            )

        next_page = response.xpath(
            '(//div[@role="navigation"]//a)[last()]/@href').extract_first()
        if next_page:
            yield response.follow(
                url=next_page, headers=self.headers, callback=self.parse_link
            )

    def parse(self, response, category_url):

        item = OlxQaItem()
        ad_id = ' '.join(map(str, response.xpath(
            "//div[text()[contains(.,'Ad id')]]/text()").re(r"\d+")))
        # api_request = "https://www.olx.qa/api/listing/?external_id=" + ad_id
        # yield scrapy.Request(url=api_request, callback=self.parse,cb_kwargs={'category_url':url})
        # with open('datas_olx.json', 'w') as f:
        #     f.write(json.dumps(api_request, indent=4))
        # with open('datas_olx.json', 'r') as jf:
        #     for lines in jf.read():
        #         data += lines
        #     datas = json.loads(data)
        url = response.url
        broker = response.xpath(
            "//div[@aria-label='Seller description']//a//span/text()").extract_first().encode('utf-8').decode().strip()
        category = response.xpath(
            '//div[@aria-label="Breadcrumb"]//a/text()').extract()
        category_url = category_url
        title = response.xpath(
            '//h1[@class="a38b8112"]/text()').extract_first().encode('utf-8').decode().strip()
        description = response.xpath('//div[@class="_0f86855a"]/span/text()').extract_first(
        ).encode('utf-8').decode().replace('\n', '').strip()
        location = response.xpath(
            '//span[@class="_8918c0a8"]/text()').extract_first()
        price = response.xpath(
            '//span[@class="_56dab877"]/text()').extract_first().replace(',', '').split(' ')

        for price_dict in range(len(price)):

            price_dict = {'price': float(price[-1]), 'currency': price[0]}

        amenity = response.xpath(
            '//div[@class="_4ab34fd4"]//span/text()').extract()
        amenities = amenity if amenity else 'N/A'
        details = response.xpath(
            '//div[@class="_241b3b1e"]//span/text()').extract()
        details_dict = {details[detail].encode("ascii", "ignore").decode().strip(): details[detail + 1]
                        for detail in range(0, len(details), 2)}
        imgs = response.xpath(
            "//div[@class='image-gallery-swipe']//img/@src").extract()
        img = response.xpath(
            "//div[@aria-label='Gallery']//img/@src").extract()
        if imgs:
            number_of_photos = len(imgs)
        elif img:
            number_of_photos = len(img)
        published_on = response.xpath(
            "//span[@class='_8918c0a8']/span/text()").extract_first()
        item['id'] = ad_id
        item['url'] = url
        item['category'] = category
        item['category_url'] = category_url
        item['title'] = title
        item['description'] = description
        item['location'] = location
        item['price'] = price_dict
        item['amenities'] = amenities
        item['details'] = details_dict
        item['number_of_photos'] = number_of_photos
        item['published_at'] = published_on
        yield item
