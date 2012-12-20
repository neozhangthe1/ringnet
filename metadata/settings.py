'''
Created on Dec 19, 2012

@author: Yutao
'''
DB_HOST = "10.1.1.110"
DB_USER = "root"
DB_PORT = 3306
DB_PASS = "keg2012"
DB_NAME = "arnet_db"

MONGO_HOST = "10.1.1.110"
MONGO_NAME = "scrapy"

import os
HERE = os.path.abspath(os.curdir)
PROJ_PATH = os.path.split(HERE)[0]
DATA_PATH = os.path.join(PROJ_PATH, "data").replace('\\','/')
DOC_PATH = os.path.join(DATA_PATH, "docs").replace('\\','/')
GRAPH_PATH = os.path.join(DATA_PATH, "graph").replace('\\','/')
COMMUNITY_PATH = os.path.join(DATA_PATH, "community").replace('\\','/')