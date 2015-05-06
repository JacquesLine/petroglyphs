#!/usr/bin/python2
# -*-coding:Utf-8 -*

import cv2
import numpy as np
from skimage import morphology
from skimage import img_as_ubyte
import sys
import os.path

def skeletonFinal(img,n,k):

	# Loading and denoising the photo
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.threshold(img, 0, 100, cv2.THRESH_OTSU)[1]
	dst = cv2.fastNlMeansDenoising(img,None,n,7,21)
	# Skeletonizing
	im = cv2.threshold(dst, 0, k, cv2.THRESH_OTSU)[1]
	im = morphology.skeletonize(im > 0)
	imcv = img_as_ubyte(im)
	#cv2.imwrite("dst.bmp", imcv)
	return imcv


# Main
if __name__ == "__main__":
    for image in sys.argv[1:]:
        im = cv2.imread(image)
        skeletonFinal(im,200,200)
        s_im = cv2.imread("dst.bmp")
        name = "Output/"+ os.path.basename(image[0:(len(image)-4)]) + ".png"
        cv2.imwrite(name, s_im)

