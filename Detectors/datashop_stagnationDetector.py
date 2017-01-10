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

detectorName = "stagnation" # provide name for each detector

teacherActionSet = set([]) #do not touch

def runDetector(inputString):

	dataShopDataset_path = inputString
	thisFileName = inputString.split("/")[-1]
	rootPathName = ("/").join(inputString.split("/")[:-2])
	target_path = rootPathName + "/Annotated_Datasets" + "/" + thisFileName + "_" + detectorName + ".txt"

	prevTime = {}
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
			currTime = row[headers.index("CF (tool_event_time)")]
			currTime = datetime.strptime(currTime.split(" ")[1].split(".")[0], "%X")
			currOutcome = row[headers.index("Outcome")]

			if currOutcome != "":
				if stuID not in prevTime.keys():
					classState[stuID] = 0.0
				else:
					#if "-1 day" in str(currTime - prevTime[stuID]):
					#	print row[headers.index("CF (tool_event_time)")], currTime, prevTime[stuID]
					for item in classState.keys():
						classState[item] = (currTime - prevTime[item]).total_seconds()
				prevTime[stuID] = currTime

			#write augmented row
	   		writer0.writerow(row + [str(classState)])

	return target_path, teacherActionSet