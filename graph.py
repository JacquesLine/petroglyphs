#!/usr/bin/python2
# -*-coding:Utf-8 -*

import math
import os
import shapely.geometry as geometry
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from graph_util import *

"""
This script transforms a skeleton of a picture into a networkx graph
Inputs: 
'name' name of the path of a picture
'k1' parameter for the cleaning of the graph, higher is n, stronger is the cleaning of the graph
Output:
'k2' parameter for the detection of curves, lower is n, more precise will be the detection
Output:
networkx graph of boolPoint objects 
"""

def skeletonToGraph(name,k1,k2):

	#Initialisation
	im = Image.open(name)
	im = im.convert("L")
	imageW = im.size[0]
	imageH = im.size[1]
	image = [[[0,False] for i in range(0,imageH)] for j in range(0,imageW)]
	nodes = list()
	edges = list()
	graph = nx.Graph()

	#Detection of the graph nodes
	for y in range(0,imageH):
		for x in range(0, imageW):
			if im.getpixel((x,y))>0:
				image[x][y] = [1,True]
				point = boolPoint(x,y)
				l,n=point.neighbours(im)	
				if n==2 or n>3:
					if n==2:
						point.status = "e"
					else:
						point.status = "b"
					nodes.append(point)
					

	for node in nodes:
		image[node.x][node.y]=[2,True]

	#Reorder the nodes
	nodes = reorder(nodes)	

	#Detection of the graph edges
	test = True
	while test:
		edges,nodes,test = getEdges(image,nodes,k2)
		resetMatrix(image,imageH,imageW,nodes)
		
	#Clean the graph: merge close nodes
	nodes,edges = clean(nodes,edges,k1)
	
	#Create a networkx graph
	opt_nodes,opt_edges = [],[]
	for edge in edges:
		opt_edges.append(((edge[0].x,edge[0].y),(edge[1].x,edge[1].y)))
	for node in nodes:
		opt_nodes.append((node.x,node.y))
	graph.add_nodes_from(opt_nodes)
	graph.add_edges_from(opt_edges)

	"""for edge in edges:
		plot(edge)
	plt.show()"""

	return graph
