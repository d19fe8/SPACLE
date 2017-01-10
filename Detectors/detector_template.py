import sys
import os
import csv
import random
from time import sleep
import numpy as np
import cv2
import copy
from datetime import datetime
dir = os.path.dirname(__file__)

detectorName = #insert detector name here

teacherActionSet = set([]) #do not touch

def runDetector(inputString):

	dataShopDataset_path = inputString
	target_path = inputString.split(".")[0] + "_" + detectorName + ".txt"

	history = {}
	classState = {}

	with open(target_path, 'wb') as outputFile:
		f = open(dataShopDataset_path, 'rU')
		reader = csv.reader(f, delimiter='\t',quoting=csv.QUOTE_NONE)
		writer0 = csv.writer(outputFile, delimiter='\t')

		headers = reader.next()
		writer0.writerow(headers + ["classState"])
		for row in reader:
			#get row variables...
			stuID = row[headers.index("Anon Student Id")]
			teacherAction = row[headers.index("What is teacher doing")]
			if teacherAction not in teacherActionSet:
				teacherActionSet.add(teacherAction)
			#add more row variables here...

			#insert processing code here...

			#write augmented row
	   		writer0.writerow(row + [str(classState)])

	return target_path, teacherActionSet