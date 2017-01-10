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

detectorName = "recent_hint_frequency" #insert detector name here

teacherActionSet = set([]) #do not touch

def runDetector(inputString):

	dataShopDataset_path = inputString
	thisFileName = inputString.split("/")[-1]
	rootPathName = ("/").join(inputString.split("/")[:-2])
	target_path = rootPathName + "/Annotated_Datasets" + "/" + thisFileName + "_" + detectorName + ".txt"

	history = {}
	classState = {}
	classStateWindow = {}

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
			isStuAction  = row[headers.index("Step Name")]!=""
			isHelpRequest = row[headers.index("Student Response Type")]=="HINT_REQUEST"

			#insert processing code here...
			if stuID not in classState.keys():
		 		classState[stuID] = 0.0
		 		classStateWindow[stuID] = [0.0, 0.0, 0.0, 0.0]
			else:
				if isStuAction:
					if isHelpRequest:
						classStateWindow[stuID].pop()
						classStateWindow[stuID].append(1.0)
					else:	
						classStateWindow[stuID].pop()
						classStateWindow[stuID].append(0.0)
			classState[stuID] = sum(classStateWindow[stuID])

			#write augmented row
	   		writer0.writerow(row + [str(classState)])

	return target_path, teacherActionSet