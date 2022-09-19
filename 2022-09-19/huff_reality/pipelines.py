# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

# from scrapy.conf import settings
# from scrapy import log
# from scrapy.exceptions import DropItem


# class MongoDBPipeline(object):

#     def __init__(self):

#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DB']]
#         self.collection = db[settings['MONGODB_COLLECTION']]

    # def process_item(self, item, spider):

    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem("Missing {0}!".format(data))
    #     if valid:
    #         self.collection.insert(dict(item))
    #         log.msg(" added to MongoDB database!",
    #                 level=log.DEBUG, spider=spider)
    #     return item


class HuffRealityPipeline:

    def __init__(self):

        self.conn = pymongo.MongoClient(
            'localhost',
            27017)
        db = self.conn['huffreality']
        self.collection = db['agents']

    def process_item(self, item, spider):

        self.collection.insert_one(dict(item))
        return item
