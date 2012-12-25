'''
Created on Dec 19, 2012

@author: Yutao
'''

from metadata import settings
from metadata import verbose
import os
import numpy as np
from sklearn.cluster import spectral_clustering
from scipy.sparse import lil_matrix

class Community(object):
    def __init__(self, year, id, index):
        self.id = id
        self.index = index
        self.year = year
        self.members = []
    
    def append_member(self,member):
        self.members.append(member)
        
    def intersect(self, comm):
        return len(set(self.members) & set(comm.members))
    
    def to_string(self):
        s = str(self.index)+" "+str(self.year)+" "+str(self.id)+" "
        for m in self.members:
            s+=str(m)+','
        return s
    
def gen_weight_graph():
    pass
    
def community_clustering_modularity():
    import networkx as nx
    import louvain
    path = settings.COMMUNITY_PATH
    verbose.debug(path)
    index = 0
    communities = []
    merged_communities = {}
    for root, dirs, files in os.walk(path):
        for year in files:
            verbose.debug(year)
            merged_communities[int(year)] = [[] for i in range(200)]
            comm_dict = {}
            input = open(os.path.join(path,year))
            for line in input:
                x = line.strip().split(' ')
                author = int(x[0])
                id = int(x[1])
                if not comm_dict.has_key(id):
                    comm_dict[id] = Community(int(year),id,index)
                    index+=1
                comm_dict[id].append_member(author)
            for id in comm_dict.keys():
                communities.append(comm_dict[id])
    verbose.debug("num of communities: "+str(len(communities)))
    g = nx.Graph()
    for i in range(len(communities)):
        for j in range(i+1,len(communities)):
            affinity = communities[i].intersect(communities[j])
            if affinity!=0:
                g.add_edge(i,j,weight=affinity)
    louvain.detect(g, settings.COMMUNITY_PATH+"\\modularity_clusters")

def community_clustering():
    path = settings.COMMUNITY_PATH
    verbose.debug(path)
    index = 0
    communities = []
    merged_communities = {}
    for root, dirs, files in os.walk(path):
        for year in files:
            verbose.debug(year)
            merged_communities[int(year)] = [[] for i in range(200)]
            comm_dict = {}
            input = open(os.path.join(path,year))
            for line in input:
                x = line.strip().split(' ')
                author = int(x[0])
                id = int(x[1])
                if not comm_dict.has_key(id):
                    comm_dict[id] = Community(int(year),id,index)
                    index+=1
                comm_dict[id].append_member(author)
            for id in comm_dict.keys():
                communities.append(comm_dict[id])
    verbose.debug("num of communities: "+str(len(communities)))
    adjacency = lil_matrix((len(communities),len(communities)))
    for i in range(len(communities)):
        for j in range(i+1,len(communities)):
            affinity = communities[i].intersect(communities[j])
            adjacency[i,j]=affinity
            adjacency[j,i]=affinity
    labels = spectral_clustering(adjacency, n_clusters = 200)
    verbose.debug("clustering finished")
    for i in range(len(labels)):
        merged_communities[communities[i].year][labels[i]].extend(communities[i].members)
    for year in merged_communities.keys():
        cluster_file = open(settings.DATA_PATH+"\\clusters\\"+str(year), 'w')
        for i in range(len(merged_communities[year])):
            [cluster_file.write(str(member)+',') for member in merged_communities[year][i]]                     

def main():
    community_clustering()


if __name__ == "__main__":
    main()