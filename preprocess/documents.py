'''
Created on Dec 19, 2012

@author: Yutao
'''
from metadata import settings
from database.mysql import Mysql

SQL_GET_AUTHOR_PUB = "SELECT * FROM na_author2pub"
SQL_GET_PUB_YEAR = "SELECT id, year FROM publication"
mysql = Mysql()
cur = mysql.cur

def doc_to_bag_of_words():
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.datasets import load_files
    docs = load_files(settings.DOC_PATH)

def get_author_pub():
    cur.execute(SQL_GET_AUTHOR_PUB)
    author_pub_file = open(settings.DATA_PATH+"\\authorPub.txt",'w')
    coauthors_file = open(settings.DATA_PATH+"\\coauthors.txt",'w')
#    author_rel_file = open(settings.DATA_PATH+"\\authorRel.txt",'w')
    pubs = {}
    for rel in cur.fetchall():
        print str(rel[0])
        if pubs.has_key(rel[2]):
            pubs[rel[2]].append(rel[1])
        else:
            pubs[rel[2]]=[rel[1]]
        author_pub_file.write(str(rel[1])+' '+str(rel[2])+'\n')
    print "[DEBUG]get coauthors started"
    for key in pubs.keys():
        print str(key)
        coauthors_file.write(str(key)+':')
        for author in pubs[key]:
            coauthors_file.write(str(author)+' ')
        coauthors_file.write('\n')
    coauthors_file.close()
    author_pub_file.close()    
    
def get_author_rel():
    pub2year = {}
    year2file = {}
    pub_year = open(settings.DATA_PATH+"\\pubYear.txt")
    coauthors = open(settings.DATA_PATH+"\\coauthors.txt")
    for line in pub_year:
        x = line.strip().split(' ')
        pub2year[x[0]] = x[1]
        if not year2file.has_key(x[1]):
            year2file[x[1]] = open(settings.DATA_PATH+"\\authorRel\\"+x[1],'w')
    for line in coauthors:
        x = line.strip().split(':')
        try:
            year = pub2year[x[0]]
            out = year2file[year]
            print x[0]
            authors = x[1].split(' ')
            for i in range(len(authors)):
                for j in range((i+1),len(authors)):
                    out.write(authors[i]+' '+authors[j]+'\n')
        except Exception, e:
            print e     

def gen_graph():
    import os
    dir = settings.DATA_PATH+"\\graph\\"
    rel_dir = settings.DATA_PATH+"\\authorRel\\"
    for root, dirs, files in os.walk(rel_dir):
        for f in files:
            out = open(dir+f,'w')
            rels = open(rel_dir+f)
            relation = {}
            for line in rels:
                x = line.strip().split(' ')
                if relation.has_key(x[0]):
                    if relation[x[0]].has_key(x[1]):
                        relation[x[0]][x[1]]+=1
                    else:
                        relation[x[0]][x[1]]=1
                else:
                    relation[x[0]]={x[1]:1}
            for key1 in relation.keys():
                print key1
                print len(relation[key1])
                for key2 in relation[key1].keys():
                    out.write(key1+' '+key2+' '+str(relation[key1][key2])+'\n')                
    

def get_publication_info():
    cur.execute(SQL_GET_PUB_YEAR)
    pub_year_file = open(settings.DATA_PATH+"\\pubYear.txt",'w')
    for row in cur.fetchall():
        print row[0]
        pub_year_file.write(str(row[0])+' '+str(row[1])+'\n')

def split_by_author():
    pass

def split_by_year():
    pass

def split_docs():
    index = 0
    topic_file = open(settings.DATA_PATH+"\\docTopic.txt")
    for line in topic_file:
        x = line.strip().split('#')
        print index
        index+=1
        print x[0]
        out = open(settings.DOC_PATH+x[0],'w')
        out.write(x[1])
        out.close()
        
def merge_docs(docs):
    merge_file = open(settings.DATA_PATH+"\\sampleDocs.txt",'w')
    for doc in docs:
        input = open(settings.DOC_PATH+str(doc))
        for line in input:
            merge_file.write(str(doc)+'#'+line.strip()+'\n')
    merge_file.close()
        

def main():
    gen_graph()

if __name__ == "__main__":
    main()