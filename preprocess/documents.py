'''
Created on Dec 19, 2012

@author: Yutao
'''
from metadata import settings
from metadata import verbose
from database.mysql import Mysql
import codecs
import os
from bs4 import UnicodeDammit



SQL_GET_AUTHOR_PUB = "SELECT * FROM na_author2pub"
SQL_GET_PUB_YEAR = "SELECT id, year FROM publication"
SQL_PUBLICATION_TITLE_ABSTRACTRS = "SELECT p.id, p.title, p.abstract FROM publicat_ext_ext1 p where p.year>=2000 and p.year<2010";
mysql = Mysql()
cur = mysql.cur

def get_paper_content():
    papers = mysql.get_paper_content()
    for paper in papers:
        doc = open("D:\\share\\yutao\\Workspace\\data\\"+paper,"w")
        doc.write(papers[paper])
        doc.close()

def get_title_abstract():
    cur.execute(SQL_PUBLICATION)

def loaddata():
    docids = []
    docs = []
    cur.execute(SQL_PUBLICATION_TITLE_ABSTRACTRS)
    for row in cur.fetchall():
        print row[0]
        docids.append(row[0])
        data = ""
        if row[1]!=None:
            data += row[1]
        if row[2]!=None:
            try:
                data += row[2]
            except Exception,e:
                print e
        docs.append(UnicodeDammit(data).markup)
    return docids, docs
        
def doc_to_bag_of_words_db(docids,docs):
    from sklearn.feature_extraction.text import CountVectorizer
    voc = open(settings.TOPICMODEL_PATH+"\\alphabet.txt")
    vocabulary = {}
    line_count = 0
    for line in voc:
        vocabulary[line.strip()]=line_count
        line_count+=1
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    counts = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names()
    out_counts = open(settings.DATA_PATH+"\\bag_of_words",'w')
    out_sum_counts = open(settings.DATA_PATH+"\\sum_word_count",'w')
    sum_counts = counts.sum(axis=0)
    
    nonzero_count = counts.nonzero()
    id = nonzero_count[0][0]
    out_counts.write(str(docids[id])+':')
    out_counts.write(feature_names[nonzero_count[1][0]]+','+str(counts.getrow(id)[0,nonzero_count[1][0]])+'#')
    for i in range(1,len(nonzero_count[0])):
        if id!=nonzero_count[0][i]:
            id = nonzero_count[0][i]
            out_counts.write("\n")
            out_counts.write(str(docids[id])+':')
        out_counts.write(feature_names[nonzero_count[1][i]]+','+str(counts.getrow(id)[0,nonzero_count[1][i]])+'#')
    
    for i in range(sum_counts.shape[1]):
        out_sum_counts.write(feature_names[i]+' '+str(sum_counts[0,i])+'\n')

def doc_to_bag_of_words():
    from sklearn.feature_extraction.text import CountVectorizer
    voc = open(settings.TOPICMODEL_PATH+"\\alphabet.txt")
    print settings.TOPICMODEL_PATH+"\\alphabet.txt"
    vocabulary = {}
    line_count = 0
    for line in voc:
        vocabulary[line.strip()]=line_count
        line_count+=1
    print line_count
    vectorizer = CountVectorizer(min_df=1,vocabulary=vocabulary)
    docids = []
    docs = []
    for root, dirs, files in os.walk(settings.DOC_PATH):
        for file in files:
            verbose.debug(file)
            docids.append(int(file))
            docs.append(UnicodeDammit(open(os.path.join(settings.DOC_PATH,file)).read()).markup)
    counts = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names()
    out_counts = open(settings.DATA_PATH+"\\bag_of_words",'w')
    out_sum_counts = open(settings.DATA_PATH+"\\sum_word_count",'w')
    arr_counts = counts.toarray()
    sum_counts = counts.sum(axis=0)
    for i in range(len(docs)):
        out_counts.write(docids[i]+':')
        verbose.debug(docids[i])
        for j in range(len(feature_names)):
            if arr_counts[i,j]!=0:
                verbose.debug(feature_names[j]+','+str(arr_counts[i,j]))
                out_counts.write(feature_names[j]+','+str(arr_counts[i,j])+'.')
    for i in range(len(arr_counts[0])):
        out_sum_counts.write(feature_names[i]+' '+str(sum_counts[0,i])+'\n')
    
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
    doc_to_bag_of_words_db()

if __name__ == "__main__":
    main()