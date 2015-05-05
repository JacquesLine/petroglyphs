#!/usr/bin/python2
# -*-coding:Utf-8 -*


import numpy as np
import cv2
from graph import*

"""
This function divides a pictures with several petroglyphs and retunr all the graphs of each petroglyph in a list of
ntworkx graphs.
It uses cv2 findContours function
"""


def testRectangle(rectangle,y,x):
	output = False
	if (rectangle[0] <= x <= rectangle[0] + rectangle[2]) and (rectangle[1] <= y <= rectangle[1] + rectangle[3]):
		output = True
	return output

def petroglyphRecognition(name,k1,k2):

	im = cv2.imread(name)
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,im = cv2.threshold(imgray,127,255,0)
	contours, hierarchy = cv2.findContours(im.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


	rectangles = []
	graphs = []

	for contour in contours:
		i,j,w,h = cv2.boundingRect(contour)
		rectangles.append([i,j,w,h])


	for rectangle in rectangles:
		print(rectangle)
		im2 = im.copy()
		imageW = im2.shape[0]
		imageH = im2.shape[1]
		print(imageW,imageH)
		for y in range(0,imageH):
			for x in range(0, imageW):
				if im2.item(x,y) > 0 :
					if testRectangle(rectangle,x,y):
					if not testRectangle(rectangle,x,y):
						im2.itemset((x,y),0)

		cv2.imwrite("inter.png",im2)
		graph = skeletonToGraph("inter.png",k1,k2)
		graphs.append(graph)

return graphs

