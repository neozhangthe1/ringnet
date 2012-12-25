'''
Created on Dec 19, 2012

@author: Yutao
'''

from database.mysql import Mysql
from database.mongo import Mongo
from metadata import settings
from metadata import verbose
import pickle

authors = [324696,162800,113059,412623,496532,1128214,406745,225691,379284,1385190,745329,265966]
names= ["Anil K. Jain","Hector Garcia Molina","Christos Papadimitriou",
        "J. D. Ullman","Lotfi Asker Zadeh","Wei Wang","Hai Jin","Jing Zhang",
        "Bjorn Hartmann","Yunhao Liu","Jiawei Han","Philip S. Yu"]
#authors = [745329]
#names = ["Jiawei Han"]

mongo = Mongo()
mysql = Mysql()

def get_author_topic():
    pass

def select_topic(topics,selected):
    selected_topics = {}
    for s in selected:
        selected_topics[s]=topics[s]
    return selected_topics

def get_paper_topic():
    dump_file = open("E:\\My Projects\\Eclipse Workspace\\ringnet\\preprocess\\author_paper_sample")
    author_papers = pickle.load(dump_file)
    papers = set()
    for a in author_papers.keys():
        verbose.debug(a)
        for year in author_papers[a]:
            verbose.debug(year)
            for p in author_papers[a][year]:
                papers.add(p)
    paper_topic = {}
    top_topic = {}
    for p in papers:
        try:
            res = mongo.db['doc_topic200'].find({'_id':p}).next()
            paper_topic[p] = res['topics']
            top_topic[p] = res['top_topics'] 
        except Exception, e:
            print e
            print p
        
        
    author_topic = {}
    for a in author_papers.keys():
        verbose.debug('author')
        verbose.debug(a)
        topics = {}
        for i in range(2000,2010):
            topics[i]={}
            for j in range(200):
                topics[i][j] = 0.0
        for year in author_papers[a].keys():
            for p in author_papers[a][year]:
                verbose.debug('paper')
                verbose.debug(p)
                if paper_topic.has_key(p):
                    ts = paper_topic[p]
                    for t in range(len(ts)):
                        topics[year][t]+=ts[t]
                    print "found"
                else:
                    print "not found"
        author_topic[a] = topics
        
    dump_file = open('author_topic','w')
    pickle.dump(author_topic, dump_file)
    topic_weight = {}
    for i in range(2000,2010):
        topic_weight[i] = [0.0 for j in range(200)]
    for a in author_topic.keys():
        for year in author_topic[a].keys():
            for t in range(200):
                topic_weight[year][t]+=author_topic[a][year][t]
    
    dump_file = open('topic_weight','w')
    pickle.dump(topic_weight, dump_file)
    
    pattern = {"anchors":{}, "items":[], "links":[], "trajectories":[]}
    for a in range(10):
        pattern['anchors'][a] = [{"year":year,"weight":topic_weight[year][a]*10} for year in range(2000,2010)]
        
    index = 0
    
    selected_topics = [109,118]
    for i in range(len(authors)):
        a = authors[i]
        traj = []
        sum_list = {}
        for year in author_topic[a]:
            pattern['items'].append({'name':names[i],
                                     'year':year,
                                     'weight':sum(author_topic[a][year])})                                    
            print a
            print year
            for t in selected_topics:
                pattern['links'].append({'source':t-109,
                                         'target':index,
                                         'offset':year-2000,
                                         'weight':author_topic[a][year][t]})
            traj.append(index)
            index+=1
        pattern['trajectories'].append(traj)
    pattern['meta'] = {"num":10}
    
    for i in range(len(authors)):
        a = authors[i]
        traj = []
        sum_list = {}
        for year in author_topic[a]:
            pattern['items'].append({'name':names[i],
                                     'year':year,
                                     'weight':sum(author_topic[a][year])})                                    
            sum_t = max(author_topic[a][year][:10])
            print a
            print year
            print sum_t
            if sum_t == 0:
                for y in range(year, 2000):
                    if sum_list[y]>0:
                        sum_t = sum_list[y]
                        for t in range(10):
                            if author_topic[a][y][t]/sum_t<0.4:
                                pattern['links'].append({'source':t,
                                     'target':index,
                                     'offset':year-2000,
                                     'weight':0})
                            else:
                                pattern['links'].append({'source':t,
                                                         'target':index,
                                                         'offset':year-2000,
                                                         'weight':author_topic[a][y][t]})
            else:
                sum_list[year] = sum_t
                l_year = year - 1 if year > 2000 else year
                if max(author_topic[a][l_year][:10]) == 0:
                    l_year = year
                r_year = year + 1 if year < 2009 else year
                if max(author_topic[a][r_year][:10]) == 0:
                    r_year = year
                for t in range(10):
                    if author_topic[a][year][t]/sum_t<0.4:
                        pattern['links'].append({'source':t,
                             'target':index,
                             'offset':year-2000,
                             'weight':0})
                    else:
                        smooth_w = (2*author_topic[a][year][t]+author_topic[a][l_year][t]+author_topic[a][r_year][t])/4
                        pattern['links'].append({'source':t,
                                                 'target':index,
                                                 'offset':year-2000,
                                                 'weight':smooth_w})
            traj.append(index)
            index+=1
        pattern['trajectories'].append(traj)
    pattern['meta'] = {"num":10}
    
    import json
    
    json_dump = open("E:\\Dropbox\\Projects\\ringnet\\etc"+"\\109-118topic.json",'w')
    s = json.dumps(pattern)
    json_dump.write(s)
    json_dump.close()
        
    #output author_topic
    for a in author_topic:
        author_topic_dump = open("E:\\Dropbox\\Projects\\ringnet\\etc"+"\\"+"topics-"+names[authors.index(a)]+'-'+str(a)+'-200','w')
        s = json.dumps(author_topic[a])
        author_topic_dump.write(s)
        author_topic_dump.close()
        
    #plot author_topic
    import matplotlib.pyplot as plt
    for a in author_topic:
        fig = plt.figure(figsize=(50,10))
        plt.xlabel("topic id")
        plt.ylabel("topic weight")
        plt.xticks(range(0, 200, 5))
        for year in author_topic[a]:
            plt.plot(range(0,200), author_topic[a][year].values())
        plt.savefig("E:\\Dropbox\\Projects\\ringnet\\etc"+"\\"+"topics-"+names[authors.index(a)]+'-'+str(a)+'-200.png')
        plt.close()
            
    for year in range(2000,2010):
        fig = plt.figure(figsize=(50,10))
        plt.xlabel("topic id")
        plt.ylabel("topic weight")
        plt.xticks(range(0, 200, 5))
        for a in author_topic:
            plt.plot(range(0,200), author_topic[a][year].values())
        plt.savefig("E:\\Dropbox\\Projects\\ringnet\\etc"+"\\"+"topics-"+str(year)+'-200.png')
        plt.close()
        
def get_person_papers():
    author_papers = {}
    for author in authors:
        verbose.debug(author)
        papers = mysql.get_person_publications(author)
        author_papers[author]=papers
    dump_file = open("author_paper_sample",'w')
    pickle.dump(author_papers, dump_file)

def main():
    get_person_papers()

if __name__ == "__main__":
    main()