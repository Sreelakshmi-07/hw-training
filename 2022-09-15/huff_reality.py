import scrapy
import pymongo


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

            title = agents.xpath(
                './/div[@class="rn-agent-title"]/span/text()'
            ).extract_first(default='N/A').encode("ascii","ignore").decode()
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
            languages = ' '.join((map(str,language))).strip()

            yield{
                't': title,
                'o': office_name
            }
