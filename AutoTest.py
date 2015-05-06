#!/usr/bin/python2
# -*-coding:Utf-8 -*

import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
from weka.classifiers import Evaluation
from weka.core.classes import Random

from imageToData import *


jvm.start()
data_dir = "/home/antoine/Documents/Petroglyphs/petroglyphs/"


loader = Loader(classname = "weka.core.converters.ArffLoader")
cls = Classifier(classname = "weka.classifiers.lazy.IBk", options = ["-K","5","-W","0","-X"])

l1 = [300]
l2 = [5,10,15,20]
results = []
images = sys.argv[1:]

for k1 in l1:
	for k2 in l1:
		for k3 in l2:
			for k4 in l2:
				imageToData(images,k1,k2,k3,k4)
				data = loader.load_file(data_dir + "finalOutput.arff")
				data.class_is_last()
				evl = Evaluation(data)
				evl.crossvalidate_model(cls, data, 10, Random(1))
				r=evl.percent_correct
				print(k1,k2,k3,k4,r)
				results.append([k1,k2,k3,k4,r])


jvm.stop()
