'''
Created on Dec 18, 2012

@author: Yutao
'''
from metadata import settings
import MySQLdb

SQL_GET_PUBLICATION = "SELECT id,title,jconf FROM publication"
SQL_GET_ABSTRACT = "SELECT abstract FROM publication_ext WHERE id = %s"
SQL_GET_JCONF_NAME = "SELECT name FROM jconf WHERE id = %s"

class Mysql(object):
    def __init__(self):
        self.SQL_GET_PERSON_PUBLICATION = "SELECT ap.pid, p.`year` FROM na_author2pub ap, publication p WHERE ap.aid = %s and p.id = ap.pid and p.`year`>=2000 and p.`year`<=2009"
        self.db = MySQLdb.connect(host=settings.DB_HOST,
                                       user=settings.DB_USER,
                                       passwd=settings.DB_PASS,
                                       db=settings.DB_NAME)
        self.cur = self.db.cursor()
        
    def get_person_publications(self,pid):
        self.cur.execute(self.SQL_GET_PERSON_PUBLICATION % pid)
        papers = {}
        for i in range(2000,2010):
            papers[i] = []
        for p in self.cur.fetchall():
            papers[p[1]].append(p[0])
        return papers
    
    def get_paper_content(self):
        self.cur.execute(SQL_GET_PUBLICATION)
        papers = {}
        for item in self.cur.fetchall():
            content = item[1]+'\n'
            pid = item[0]
            self.cur.execute(SQL_GET_ABSTRACT % pid)
            for abs in self.cur.fetchall():
                content+=abs[0]
                content+="\n"
            self.cur.execute(SQL_GET_JCONF_NAME % item[2])
            for jconf in self.cur.fetchall():
                content+=jconf[0]
                content+="\n"
            papers[pid]=content            
        return papers