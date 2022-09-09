# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonInPipeline(object):
    # def __init__(self):
    #     self.results = []
    def process_item(self, item, spider):
        # self.results.append(item['result'])
        return item
    # def close_spider(self, spider):
    #     print(f"full result set is {self.results}")
