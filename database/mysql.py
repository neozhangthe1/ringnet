'''
Created on Dec 18, 2012

@author: Yutao
'''
from metadata import settings
import MySQLdb

class Mysql(object):
    def __init__(self):
        self.db = MySQLdb.connect(host=settings.DB_HOST,
                                       user=settings.DB_USER,
                                       passwd=settings.DB_PASS,
                                       db=settings.DB_NAME)
        self.cur = self.db.cursor()