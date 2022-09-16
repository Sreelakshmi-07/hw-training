import scrapy
import pymongo
from ..items import HuffRealityItem

class HuffReality(scrapy.Spider):

    name = 'huffreality'

    # client = pymongo.MongoClient("localhost", 27017)
    # db = client.huffreality

    headers = {
        # 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Linux"',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'cross-site',
        # 'Sec-Fetch-User': '?1',
        # 'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    base_url = 'https://www.huff.com/index.asp?p=agentResults.asp&search=%%'

    def start_requests(self):

        url = self.base_url
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):

        print(response.url)


        for agents in response.xpath('//div[@id="rnRoster"]/article'):

            item = HuffRealityItem()
            title = agents.xpath(
                    './/div[@class="rn-agent-title"]/span/text()'
            ).extract_first(default='N/A').encode(
                    "ascii", "ignore").decode().replace(
                    "- Your Real Estate Nerd", "")
            if title == "Team Website"\
                    or title == "Licensed in Kentucky & Ohio":
                title = 'N/A'
            office_name = agents.xpath(
                './/span[@class="rn-agent-contact-office-name"]/text()'
            ).extract_first()
            address = agents.xpath(
                './/span[@class="rn-agent-contact-office-address-street"]\
                /text()'
            ).extract_first()
            city = agents.xpath(
                '//div[@class="rn-agent-info"]//span[@class="rn-agent-contact-office-city-state-zip"]\
                /text()'
                ).extract_first().split(',')[0]
            state = agents.xpath('//div[@class="rn-agent-info"]//span[@class="rn-agent-contact-office-city-state-zip"]\
                /text()'
                ).extract_first().split(",")[1][0:3].strip()
            zipcode = agents.xpath('//div[@class="rn-agent-info"]//span[@class="rn-agent-contact-office-city-state-zip"]\
                /text()'
                ).extract_first().split(",")[1][4:].strip()
            # profile_url =
            language = agents.xpath('.//div[@class="rn-agent-info"]//div[@class="rn-agent-languages"]//span/text()').extract()
            languages = ' '.join((map(str,language))).strip() if language else 'N/A'
            name = agents.xpath('.//div[@class="rn-agent-info"]//span[@class="rn-agent-name"]/text()').extract_first().split()
            if len(name) < 3:
                first_name = name[0]
                last_name = name[1]
            elif len(name) > 3:
                first_name = name[0]
                middle_name = name[1]
                last_name = ' '.join(name[2:])
            else:
                first_name = name[0]
            website = agents.xpath('.//div[@class="rn-agent-icon-website"]/a/@href').extract_first()
            email = 'N/A'
            image_url = agents.xpath('.//div[@class="rn-agent-photo-languages"]/img/@src').extract_first()
            agent_phone_numbers = agents.xpath('.//span[@class="rn-agent-contact-main-phone-number"]/text()').extract_first()
            office_phone_numbers = agents.xpath('.//span[@class="rn-agent-contact-office-phone-number"]/text()').extract_first()
            country = 'United States'
            agents ={
            item['title'] : title,
            item['office_name'] : office_name,
            item['address'] : address,
            item['city'] : city,
            item['state'] : state,
            item['zipcode'] : zipcode
            }
            yield response.follow(url=website,headers=self.headers,callback=self.parse_details,meta = {agents:agents
                })

    def parse_details(self,response):
        item = HuffRealityItem()
        description = ''.join(response.xpath('//div[@class="site-home-page-content-text"]/p/text()').extract()).encode("ascii","ignore").decode()
        social = response.xpath('//ul[@class="no-bullet footer-social"]//a/@href').extract()
        item['title'] = response.meta.get(agents['item["title"]'])
        item['description'] = description
        yield item




