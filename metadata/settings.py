'''
Created on Dec 19, 2012

@author: Yutao
'''
DB_HOST = "10.1.1.110"
DB_USER = "root"
DB_PORT = 3306
DB_PASS = "keg2012"
DB_NAME = "arnet_db"

MONGO_HOST = "localhost"
MONGO_NAME = "ringnet"

import os
HERE = os.path.abspath(os.curdir)
PROJ_PATH = os.path.split(HERE)[0]
DATA_PATH = os.path.join(PROJ_PATH, "data").replace('\\','/')
DOC_PATH = "E:\\Data\\RingNet\\docs"
TOPICMODEL_PATH = "E:\\Data\\RingNet\\topicmodel\\output200"
GRAPH_PATH = os.path.join(DATA_PATH, "graph").replace('\\','/')
COMMUNITY_PATH = os.path.join(DATA_PATH, "community").replace('\\','/')

DROPBOX = "E:\\Dropbox\\Projects\\ringnet\\etc"