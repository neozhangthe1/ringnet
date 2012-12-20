'''
Created on Dec 18, 2012

@author: Yutao
'''
from metadata import settings
import pymongo

class Mongo(object):
    def __init__(self):
        self.con = pymongo.Connection(settings.MONGO_HOST)
        self.db = self.con[settings.MONGO_NAME]

