#!/usr/bin/python2
# -*-coding:Utf-8 -*

import math 
import os
import sys
import shapely.geometry as geometry
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import cmath
import cv2 
from PIL import Image
from createVector import *
from graph import *
from graph_util import *
from skeletonFinal import skeletonFinal

def writeGraph(v,finalOutput):
    s=str(v["numNodes"])+","+str(v["numEdges"])+","+str(v["numCycles"])+","+str(v["linkDensity"])+","+str(v["avgDegree"])+","+str(v["numLeafs"])+","+str(v["histDegree0"])+","+str(v["histDegree1"])+","+str(v["histDegree2"])+","+str(v["histDegree3"])+","+str(v["histDegree4"])+","+str(v["sMetric"])+","+str(v["graphEnergy"])+","+str(v["averageNeighDegree"])+","+str(v["averageCloseness"])+","+str(v["pearson"])+","+str(v["richClub"])+","+str(v["algConnect"])+","+str(v["diameter"])+","+str(v["avgShortPath"])+","+str(v["graphRadius"])+","+str(v["nom"])+"\n"
    with open(finalOutput,"a") as final:
        final.write(s)

# MAIN
def imageToData(images,k1,k2,k3,k4):   
	for image in images:
		im = cv2.imread(image)
		#skeletonFinal(im,k1,k2)
		#s_im = cv2.imread("dst.bmp")
		s_im = skeletonFinal(im,k1,k2)
		name = "Output/"+ os.path.basename(image[0:(len(image)-4)]) + ".png"
		cv2.imwrite(name, s_im)
		
	l=os.listdir("Output/")
	data=[]
	noms=[]

	for image in l:
		nom = image.split("_")[0]
		G=skeletonToGraph("Output/"+image,k3,k4)
		v=creationVecteur(G)
		v["nom"]=nom
		data.append(v)
		if not(nom in noms):
		    noms.append(nom)

	attrib="@relation petroglyph"+"\n"+"@attribute numNodes real"+"\n"+"@attribute numEdges real"+"\n"+"@attribute numCycles real"+"\n"+"@attribute linkDensity real"+"\n"+"@attribute avgDegree real"+"\n"+"@attribute numLeafs real"+"\n"+"@attribute histDegree0 real"+"\n"+"@attribute histDegree1 real"+"\n"+"@attribute histDegree2 real"+"\n"+"@attribute histDegree3 real"+"\n"+"@attribute histDegree4 real"+"\n"+"@attribute sMetric real"+"\n"+"@attribute graphEnergy real"+"\n"+"@attribute averageNeighDegree real"+"\n"+"@attribute averageCloseness real"+"\n"+"@attribute pearson real"+"\n"+"@attribute richClub real"+"\n"+"@attribute algConnect real"+"\n"+"@attribute diameter real"+"\n"+"@attribute avgShortPath real"+"\n"+"@attribute graphRadius real"+"\n"+"@attribute nom {"
	for nom in noms[:len(noms)-1]:
		attrib+=nom+","
	attrib += noms[len(noms)-1]+"}"+"\n"+"\n"+"@data"+"\n"

	with open("finalOutput.arff","w") as final:
		final.write(attrib)
		
	for vector in data:
		writeGraph(vector,"finalOutput.arff")
    


