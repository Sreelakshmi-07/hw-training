# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuffRealityItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    office_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    profile_url = scrapy.Field()
    languages = scrapy.Field()
    description = scrapy.Field()
    first_name = scrapy.Field()
    middle_name = scrapy.Field()
    last_name = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    image_url = scrapy.Field()
    agent_phone_numbers = scrapy.Field()
    office_phone_numbers = scrapy.Field()
    social = scrapy.Field()
    country = scrapy.Field()
    # pass
