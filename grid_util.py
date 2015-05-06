#!/usr/bin/python2
# -*-coding:Utf-8 -*

import math

def barycenter (l):
    sumx=0
    sumy=0
    for x,y in l:
        sumx+=x
        sumy+=y
    sumx/=len(l)
    sumy/=len(l)
    return sumx, sumy
        

class square:

    def __init__(self,w,h,px,py):
		self.w = w
		self.h = h
		self.px = px
		self.py = py
		
    def belongSquare(self,(x,y)):
        if (x>=self.px*self.w) and (x<=(self.px+1)*self.w) and (y>=self.py*self.h) and (y<=(self.py+1)*self.h):
            return 1
        else:
            return 0
            
class grid:
    # squares is a list of the squares of the grid, wGrid its width, hGrid, its height, m the number of squares in a row, n the number of squares in a column
    
    def __init__(self, wGrid, hGrid,m,n):
        self.squares=[]
        self.wGrid=wGrid
        self.hGrid=hGrid
        self.m=m
        self.n=n
        j=0
        while j<n:
            i=0
            while i<m:
               self.squares.append(square(math.floor(wGrid/m),math.floor(hGrid/n),i,j))
               i+=1
            j+=1
            
# function to know in which square the boolPoint is    
    def isIn(self,(x,y)):
        inSquares=[]
        inSquaresNumber=[]
        for square in self.squares:
            if square.belongSquare((x,y)):
                inSquares.append(square)
                inSquaresNumber.append((square.px,square.py))
        return inSquares, inSquaresNumber                
