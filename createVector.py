#!/usr/bin/python2
# -*-coding:Utf-8 -*

import networkx as nx
import numpy as np
import cmath 
import math

# Defining some useful functions to get the features
def numberLeaves(G):
    nl=0
    l=nx.nodes(G)
    for elt in l:
        n=1
        ite=nx.all_neighbors(G,elt)
        while 1:
            try:
                ite.next()
                n+=1
            except StopIteration: 
                n-=1
                break
        if n==1:
            nl+=1
    return nl

def graphEnergy (G):
    energy=0
    adjSpectre = nx.adjacency_spectrum(G)
    for elt in adjSpectre:
        if type(elt)!=complex:
            energy+=abs(elt)
    return energy
    
def averageNeighDegree(G):
    sum=0
    l=nx.nodes(G)
    for elt in l:
        sum+=G.degree(elt)
    avg=sum/(nx.number_of_nodes(G))
    return avg
    
def richClub(G):
    l1=nx.nodes(G)
    l2=[]
    for elt in l1:
        if G.degree(elt)>=1:
            l2.append(elt)
    if len(l2)<2:
        return 0
    else:
        adjk=G.subgraph(l2)
        phi=2*nx.number_of_edges(adjk)/(len(l2)*(len(l2)-1))  
        return phi
        
def metric(G):
    k=0
    for n1,n2 in nx.edges(G):
        k+=G.degree(n1)*G.degree(n2)
    return k

def average_closeness(G):
    sum=0
    for nod in nx.nodes(G):
        sum+=nx.closeness_centrality(G,nod)
    avg=sum/(nx.number_of_nodes(G))
    return avg    

def creationVecteur (G):
    v={}
    # Adding nodes
    nn = nx.number_of_nodes(G)
    v["numNodes"]=nn
    
    # Adding edges
    ne = nx.number_of_edges(G)
    v["numEdges"]=ne
    
    # Adding cyclomatic number
    c=nx.number_connected_components(G)
    cyclo = ne-nn+c
    v["numCycles"]=cyclo
    
    # Adding link density
    if nn==1:
        linkdensity="?"
    else:
        linkdensity = 2*ne/((nn-1)*nn)
    v["linkDensity"]=linkdensity
    
    # Adding average degree
    avgdegree = 2*ne/nn
    v["avgDegree"]=avgdegree
    
    # Adding number of leaves
    nl = numberLeaves(G)
    v["numLeafs"]=nl
    
    # Adding histogram of the nodes degree
    v["histDegree0"]=0
    v["histDegree1"]=0
    v["histDegree2"]=0
    v["histDegree3"]=0
    v["histDegree4"]=0
    histDegree=nx.degree_histogram(G)
    v["histDegree0"]=histDegree[0]
    if len(histDegree)>1:
        v["histDegree1"]=histDegree[1]
        if len(histDegree)>2:
            v["histDegree2"]=histDegree[2]
            if len(histDegree)>3:
                v["histDegree3"]=histDegree[3]
                if len(histDegree)>4:
                    v["histDegree4"]=histDegree[4]
  
    # Adding sMetric
    v["sMetric"]= metric(G)
    
    # Adding graph energy
    energ = graphEnergy (G)
    v["graphEnergy"]=energ     
    
    # Adding average of the average neighboring degrees of all nodes
    av = averageNeighDegree(G)
    v["averageNeighDegree"]=av
    
    # Adding average of closeness over all nodes
    v["averageCloseness"]=average_closeness(G)
    
    # Adding pearson coefficient for the degree sequence of all edges of the graph
    pearson = nx.degree_pearson_correlation_coefficient(G)
    if np.isnan(pearson):
        pearson = 0 
    v["pearson"]=pearson

    # Adding rich club metric for all nodes with a degree larger than 1
    rc=richClub(G)
    v["richClub"]=rc
    
    # Adding algebraic connectivity, i.e. the second smallest eigenvalue of the Laplacian
    algConnect = nx.laplacian_spectrum(G)
    algConnect = list(algConnect)
    algConnect = sorted(algConnect)
    v["algConnect"]=algConnect[1]
    
    # Adding diameter of the graph
    if nx.is_connected(G):
        diam = nx.diameter(G)
    
    else:
        diam="?"
    v["diameter"]=diam

    # Adding average shortest path
    if nx.is_connected(G):
        avgShortestPath=nx.average_shortest_path_length(G)
    
    else:
        avgShortestPath="?"
    v["avgShortPath"]=avgShortestPath
    
    # Adding graph radius
    if nx.is_connected(G):
        rad = nx.radius(G)
    else:
        rad="?"
    v["graphRadius"]=rad

    return v
    
# MAIN

"""G=nx.Graph()
nodes = [(2,7),(6,4),(18,5),(28,2),(17,5),(12,19)]
edges = [((2,7),(6,4)),((2,7),(18,5)),((6,4),(28,2)),((28,2),(17,5)),((18,5),(12,19))]
G.add_nodes_from(nodes)
G.add_edges_from(edges)
v=creationVecteur(G)
print(v)"""
                                                                                                                            






