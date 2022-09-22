import scrapy
from scrapy.http import Request
from ..items import IowarealtyagentsItem

class IowaAgents(scrapy.Spider):

    name = 'iowa'
    headers = {
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sec-gpc': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    url = 'https://www.iowarealty.com/real-estate-agents/sort-sn/'

    def start_requests(self):

        for page in range(1, 48):

            urls = self.url + str(page)
            yield Request(
                url=urls, headers=self.headers, callback=self.parse
            )

    def parse(self, response):

        if response.status == 200:
            item = IowarealtyagentsItem()
            agents_xpath = response.xpath('//div[@class="agent-info"]')
            title_xpath = 'span[@class="agent-title"]/text()'
            office_name_xpath = 'span[@class="agent-office-name"]/text()'
            agent_phone_numbers_xpath = './/a[@aria-label="mobile"]/text()'
            office_phone_numbers_xpath = './/a[@aria-label="phone"]/text()'
            profile_url_xpath = 'h2/a/@href'
            name_xpath = 'h2/a/text()'
            website_xpath = 'h2/a/@href'
            country = 'United States'
            # print(response.url)
            for agents in agents_xpath:
                title = agents.xpath(
                    title_xpath
                ).extract_first('').replace(
                    "{{AgentTitle}}", '')
                office_name = agents.xpath(
                    office_name_xpath
                ).extract_first('').replace(
                    "{{Office.Name}}", '')
                profile_url = agents.xpath(
                    profile_url_xpath
                ).extract_first('').replace(
                    "{{CustomeWebsiteUrl}}", '')
                name = agents.xpath(name_xpath).extract_first('').split()
                name = name if name else ''
                if len(name) == 2:
                    first_name = name[0]
                    middle_name = ''
                    last_name = name[1]
                elif len(name) == 3:
                    first_name = name[0]
                    middle_name = name[1]
                    last_name = ' '.join(name[2:])
                else:
                    first_name = ''.join(name)
                    middle_name = ''
                    last_name = ''
                website = agents.xpath(
                    website_xpath
                ).extract_first('').replace(
                    "{{CustomeWebsiteUrl}}", '')
                agent_phone_numbers = agents.xpath(
                    agent_phone_numbers_xpath).extract_first('').strip()
                office_phone_numbers = agents.xpath(
                    office_phone_numbers_xpath).extract_first('').strip()
                country = country

                item['title'] = title
                item['office_name'] = office_name
                item['profile_url'] = profile_url
                item['first_name'] = first_name
                item['middle_name'] = middle_name
                item['last_name'] = last_name
                item['website'] = website
                item['agent_phone_numbers'] = agent_phone_numbers
                item['office_phone_numbers'] = office_phone_numbers
                item['country'] = country
                meta = {
                    'title': item['title'],
                    'office_name': item['office_name'],
                    'profile_url': item['profile_url'],
                    'first_name': item['first_name'],
                    'middle_name': item['middle_name'],
                    'last_name': item['last_name'],
                    'website': item['website'],
                    'agent_phone_numbers': item['agent_phone_numbers'],
                    'office_phone_numbers': item['office_phone_numbers'],
                    'country': item['country']}
                # yield item

                if website:
                    yield Request(
                            url=website, headers=self.headers,
                            callback=self.parse_details, meta=meta
                    )

    def parse_details(self, response):

        if response.status == 200:
            data = response.meta
            item = IowarealtyagentsItem()
            description_xpath = response.xpath(
                '//div[@class="mdl-cell mdl-cell--12-col"]/p/text()[normalize-space()]\
                            | //div[@class="mdl-cell mdl-cell--12-col"]//span//text()[normalize-space()]'
            ).extract()
            description = ''.join(
                description_xpath).strip() if description_xpath else ''
            image_url_xpath = response.xpath(
                '//div[@class="top-agent-image"]/img/@src'
            ).extract_first('')
            address_xpath = response.xpath(
                '//li[@class="address"]/i[position() = 1]/text()'
            ).extract_first('')
            city_xpath = response.xpath(
                '//li[@class="address"]/i[position() = 2]/text()'
            ).extract_first('')
            state_xpath = response.xpath(
                '//li[@class="address"]/i[position() = 3]/text()'
            ).extract_first('')
            zipcode_xpath = int(response.xpath(
                '//li[@class="address"]/i[position() = 4]/text()'
            ).extract_first(''))
            email_xpath = response.xpath(
                '//div[@class="mdl-cell mdl-cell--12-col"]//a/text()'
            ).extract_first('').replace('CLICK HERE', '')
            social_xpath = ' '.join(
                response.xpath(
                    '//div[@class="social-icons"]/a/@href'
                ).extract()
            ).replace("#", '').split()
            social = social_xpath if social_xpath else ''

            item['title'] = data.get('title')
            item['office_name'] = data.get('office_name')
            item['address'] = address_xpath
            item['city'] = city_xpath
            item['state'] = state_xpath
            item['zipcode'] = zipcode_xpath
            item['profile_url'] = data.get('profile_url')
            item['languages'] = ''
            item['description'] = description.replace("\"", '')
            item['first_name'] = data.get('first_name')
            item['middle_name'] = data.get('middle_name')
            item['last_name'] = data.get('last_name')
            item['website'] = data.get('website')
            item['email'] = email_xpath
            item['image_url'] = image_url_xpath
            item['agent_phone_numbers'] = data.get('agent_phone_numbers')
            item['office_phone_numbers'] = data.get('office_phone_numbers')
            item['social'] = social
            item['country'] = data.get('country')
            yield item
