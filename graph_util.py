#!/usr/bin/python2
# -*-coding:Utf-8 -*

import math
from math import sqrt
import os
import sys
import shapely.geometry as geometry
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def plot(points):
	x = list()
	y = list()	
	for point in points:
		x.append(point.x)
		y.append(point.y)
	xn = np.array(x)
	yn = np.array(y)
	plt.plot(xn,yn)	
		

def clean(nodes,edges,n):
	resultEdges = edges
	finalEdges = list()
	resultNodes = list()
	resultNodes.append(nodes[0])	
	for node in nodes[1:]:
		b=True	
		for point in resultNodes:
			if abs(node.x-point.x)<n  and abs(node.y-point.y)<n:
				b=False
				for edge in resultEdges:
					if edge[0]==node:
						edge[0]=point
					if edge[1]==node:
						edge[1] = point						
		if b:				
			resultNodes.append(node)
	for edge in resultEdges:
		if edge[0] != edge[1]:
			finalEdges.append(edge)
			
	return resultNodes,finalEdges			


def reorder(nodes):
	output = list()
	for node in nodes:
		if node.status == "e":
			output.append(node)
	for node in nodes:
		if node.status == "b":
			output.append(node)
	return output
			

def followLine(node,image,nodes):
	points = list()
	node2 = boolPoint(-1,-1)
	x=node.x
	y=node.y
	image[x][y][1] = False
	x,y = next(x,y,image)
	while image[x][y][0] != 2 and next(x,y,image) != (-1,-1) :
		image[x][y][1] = False
		points.append(boolPoint(x,y))			
		x,y =next(x,y,image)
	if image[x][y][0] == 2:
		node2 = findNode(x,y,nodes)
	image[node.x][node.y][1]=True
	if node2 is None:
		node2 = boolPoint(-1,-1)
	return node2,points


def getEdges(image,nodes,m):
	edges = list()
	resultEdges = list()
	resultPoints = nodes
	test = False
	for node in nodes:
		image[node.x][node.y][1]=False
		n=1
		while neighbours(image,node.x,node.y,n) == [] and n<10:
			n+=1
		for point in neighbours(image,node.x,node.y,n):
			node2,points =followLine(point,image,nodes)
			if not (node2.x == -1 and node2.y == -1):
				point,edges = curvePoints(node,node2,points,image,m)
				if point.x != -1 and point.y != -1:
					resultPoints.append(point)
					test = True
				for edge in edges:
					resultEdges.append(edge)
		image[node.x][node.y][1]=True
	return resultEdges,resultPoints,test


def next(x,y,image):
	n=1
	while neighbours(image,x,y,n) == [] and n<10:
		n+=1
	try:	
		u=neighbours(image,x,y,n)[0].x
		v=neighbours(image,x,y,n)[0].y
	except IndexError:
		u=-1
		v=-1
	return u,v


def neighbours(image,x,y,n):
	imageW , imageH = len(image),len(image[0])
	l=list()
	if x>=n and x<(imageW-n) and y>=n and y<(imageH-n):
		for i in range(-n,n+1):
				for j in range(-n,n+1):
				
						if image[x+i][y+j][0]>0 and image[x+i][y+j][1] != False and not (i==0 and j==0):
							l.append(boolPoint(x+i,y+j))
	return l


def findNode(x,y,nodes):
	for node in nodes:
		try:
			if node.x==x and node.y==y:
				return node
		except:
			return boolPoint(0,0)




def curvePoints(start,end,points,image,m):
	resultEdges = list()
	resultPoint = boolPoint(-1,-1)
	a = end.x-start.x
	b = end.y-start.y
	c = -b*end.x +a*end.y
	vect=[b,-a,c]
	maxi,point = maxDist(vect,points)
	if maxi > m:
		image[point.x][point.y] = [2,True]
		resultEdges.append([start,point])
		resultEdges.append([point,end])
		resultPoint = point
	else:
		resultEdges.append([start,end])
	return resultPoint, resultEdges


def maxDist (vect,points):
	maxPoint = boolPoint(-1,-1)
	maxi = -1
	for point in points:
		if dist (vect,point.x,point.y) > maxi:
			maxi = dist(vect,point.x,point.y)
			maxPoint = point
	return maxi , maxPoint
		
	

def dist (vect,x,y):
	d= abs(vect[0]*x + vect[1]*y + vect[2])/sqrt(vect[0]*vect[0] + vect[1]*vect[1])
	return d



def resetMatrix(image,imageH,imageW,nodes):
	for y in range(0,imageH):
		for x in range(0, imageW):
			if image[x][y][0] > 0:
				image[x][y][0] = 1
				image[x][y][1] = True
	for node in nodes:
		image[node.x][node.y]=[2,True]

class boolPoint:

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.status = "n"
		#Status is n if the point is a normal pixel, e if it is an endpoint and b if it is a breakpoint
	
	def neighbours(self,im):
		imageW = im.size[0]
		imageH = im.size[1]
		n=0
		l=list()
		for i in [-1,0,1]:
			for j in [-1,0,1]:
			    if (self.x+i>=0) and (self.x+i<(imageW-1)) and (self.y+j>=0) and (self.y+j<(imageH-1)):
				    if im.getpixel((abs(self.x + i),abs(self.y +j)))>0:
						n+=1
						p=boolPoint(abs(self.x + i),abs(self.y + j))
						l.append(p)
		return l,n

	def __str__(self):
		return "{}	{}".format(self.x,self.y)
	
	def __repr__(self):
		return "{}	{}".format(self.x,self.y)
					
				

