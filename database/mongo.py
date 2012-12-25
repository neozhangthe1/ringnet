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

        #db
        self.doc_topic = self.db['doc_topic200']
        
        
    def store_doc_topic(self):
        col = self.db['doc_topic200']
        doc_topic = open('E:\\Data\\RingNet\\topicmodel\\output200\\docTopic.txt')
        index = 0
        for line in doc_topic:
            if index%10000==0:
                print index
            index+=1
            item = {}
            x = line.strip().split('#')
            topics = {}
            ts = x[1].split(',')
            for t in ts:
                y = t.split(':')
                topics[int(y[0])]=float(y[1])
            tl = [0.0 for i in range(200)]
            for t in topics.keys():
                tl[t]=topics[t]
            item['_id']=int(x[0])
            item['topics']=tl
            top_topics = []
            sorted_topics = sorted(topics.iteritems(), key=lambda z:z[1], reverse=True)[:10]
            item['top_topics']=sorted_topics
            col.save(item)
            
if __name__ == "__main__":
    db = Mongo()
    db.store_doc_topic()
            