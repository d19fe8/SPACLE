import sys
import os
import csv
import random
from time import sleep
from ast import literal_eval as make_tuple
import numpy as np
import cv2
import copy
import shutil
import operator
import pickle
from datetime import datetime
import Tkinter as tk
import Tkinter
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkColorChooser import askcolor  
import tkFont
import tkMessageBox
import random
from random import randint
from PIL import Image
dir = os.path.dirname(__file__)
sys.path.append(os.path.join(dir, 'Detectors'))

globalParams = {"mergedDataset": "None", "datashop_dataset": "", "classroom_observations": "", "pause_flag": True, "stuToPosPath": "", "nm": None}

stuCoords = {}

defaultParameters = {'raisedHandColor': (0,255,255), 'defaultColor': (0,255,0), 'colorStart': (0,0,0), 'colorEnd': (0,255,0), 'minValue': 60, 'maxValue': 100, 'playbackSpeed': 1000, 'refreshRate': 50}
valueColorMap = {}
colorPickerButtons = {}

#construct mapping from stuNames to DatashopIds...
stuToID = pickle.load(open("stuToID.p", "rb"))
IDToStu = {v: k for k, v in stuToID.items()}

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.configure(background='#FFFFFF')

        helvInst = tkFont.Font(family='Helvetica', size=13)
        helvHeader = tkFont.Font(family='Helvetica', size=13, weight='bold')
        circleFont = tkFont.Font(family='Helvetica', size=25, weight='bold')


        emptyLabel0 = Tkinter.Label(self, text="   ")
        emptyLabel0.grid(column=0,row=0,pady=0,padx=0)

        emptyLabel00 = Tkinter.Label(self, text="       ")
        emptyLabel00.grid(column=1,row=0,pady=10,padx=1)

        #IMPORT ROSTER
        roster_options = Tkinter.Label(self, text="Import class roster: ", font=helvHeader)
        roster_options.grid(column=1,row=1,pady=10,padx=5)
        self.button = Button(self, text="Import", width="30", command=self.load_roster)
        self.button.grid(column=2,row=1,pady=2,padx=1)
        self.roster_label = Tkinter.Label(self, text="None selected", font=helvHeader, bg="grey")
        self.roster_label.grid(column=4,row=1,pady=10,padx=5)

        emptyLabel001 = Tkinter.Label(self, text="       ")
        emptyLabel001.grid(column=1,row=2,pady=0,padx=1)

        #MAP UPLOADS
        map_options = Tkinter.Label(self, text="Select a map: ", font=helvHeader)
        map_options.grid(column=1,row=3,pady=10,padx=5)
        self.loadMapButton = Button(self, state=DISABLED, text="Import existing map", width="30", command=self.load_existing_map)
        self.loadMapButton.grid(column=2,row=3,pady=2,padx=1)
        or0_label = Tkinter.Label(self, text=" OR ", font=helvHeader)
        or0_label.grid(column=3,row=3,pady=12,padx=1)
        self.createMapButton = Button(self, state=DISABLED, text="Create new map", width="24", command=self.create_window_new_map)
        self.createMapButton.grid(column=4,row=3,pady=2,padx=1)
        #currSel1_label = Tkinter.Label(self, text="Current map selection: ", font=helvInst, bg="grey")
        #currSel1_label.grid(column=2,row=4,pady=12,padx=1)
        self.map_label = Tkinter.Label(self, text="None selected", font=helvInst, bg="grey")
        self.map_label.grid(column=4,row=4,pady=12,padx=1)

        emptyLabel01 = Tkinter.Label(self, text="       ")
        emptyLabel01.grid(column=1,row=5,pady=0,padx=1)

        #DATASET UPLOADS
        dataset_options = Tkinter.Label(self, text="Select a dataset:", font=helvHeader)
        dataset_options.grid(column=1,row=6,pady=10,padx=1)
        self.loadDatasetButton = Button(self, state=DISABLED, text="Import existing dataset", width="30", command=self.load_existing_dataset)
        self.loadDatasetButton.grid(column=2,row=6,pady=1,padx=3)
        or1_label = Tkinter.Label(self, text=" OR ", font=helvHeader)
        or1_label.grid(column=3,row=6,pady=12,padx=1)
        self.createDatasetButton = Button(self, state=DISABLED, text="Create merged dataset", width="24", command=self.create_window_merge)
        self.createDatasetButton.grid(column=4,row=6,pady=1,padx=3)
        #currSel2_label = Tkinter.Label(self, text="Current dataset selection: ", font=helvInst, bg="grey")
        #currSel2_label.grid(column=2,row=7,pady=12,padx=1)
        self.dataset_label = Tkinter.Label(self, text="None selected", font=helvInst, bg="grey")
        self.dataset_label.grid(column=4,row=7,pady=12,padx=1)

        emptyLabel02 = Tkinter.Label(self, text="       ")
        emptyLabel02.grid(column=1,row=8,pady=0,padx=1)

        #DETECTOR
        detector_options = Tkinter.Label(self, text="Select a detector: ", font=helvHeader)
        detector_options.grid(column=1,row=9,pady=10,padx=5)
        self.detectorButton = Button(self, state=DISABLED, text="Select detector", width="30", command=self.load_detector)
        self.detectorButton.grid(column=2,row=9,pady=1,padx=3)
        #currSel3_label = Tkinter.Label(self, text="Current detector selection: ", font=helvInst, bg="grey")
        #currSel3_label.grid(column=2,row=10,pady=12,padx=1)
        self.detector_label = Tkinter.Label(self, text="None selected", font=helvInst, bg="grey")
        self.detector_label.grid(column=4,row=10,pady=12,padx=1)

        emptyLabel03 = Tkinter.Label(self, text="       ")
        emptyLabel03.grid(column=1,row=11,pady=0,padx=1)

        #SET REPLAY PARAMETERS
        replay_options = Tkinter.Label(self, text="Configure replay: ", font=helvHeader)
        replay_options.grid(column=1,row=12,pady=10,padx=5)
        self.replaySettingsButton = Button(self, state=DISABLED, text="Replay settings", width="30", command=self.create_window_replay_settings)
        self.replaySettingsButton.grid(column=2,row=12,pady=1,padx=3)

        emptyLabel9 = Tkinter.Label(self, text="       ")
        emptyLabel9.grid(column=1,row=13,pady=0,padx=1)

        #RUN REPLAY
        self.replayButton = Button(self, state=DISABLED, text='Open replay', font=helvHeader, width=10, command=self.create_window_replay)
        self.replayButton.grid(column=5, row=14,pady=10,padx=12)
        #self.pauseButton = Button(self, state="normal", text='Pause/play', font=helvHeader, width=10, command=self.pause_replay)
        #self.pauseButton.grid(column=5, row=14,pady=10,padx=5)
        self.replayCloseButton = Button(self, state="normal", text='Close replay', font=helvHeader, width=10, command=self.close_replay_windows)
        self.replayCloseButton.grid(column=5, row=15,pady=10,padx=12)


    def stuNameToDatashopId(self, stuName):
        if stuName in stuToID.keys():
            stuName = stuToID[stuName]
        else:
            if stuName!="back of class" and stuName!="outside":
                print str(stuName) + " was not found in the DataShop id mapping file."
        return stuName

    def constructStuToPos(self, stuToPosPath):
        stuNameToClassPos = {}
        #open tsv file with reader
        f = open(stuToPosPath, 'rU')
        reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
        headers = reader.next()
        for row in reader:
            #take studentname from row[0] and create new entry in stuNameToClassPos for this student
            thisStu = row[headers.index("Student_Name")]
            stuNameToClassPos[thisStu] = {}
            try:
                center = tuple(map(int, eval(row[headers.index("Center_Point")])))
            except:
                center = tuple(map(int, eval(eval(row[headers.index("Center_Point")]))))
            scale = float(row[headers.index("Scale")])
            orientation = float(row[headers.index("Orientation")])
            if orientation == 0:
                stuNameToClassPos[thisStu]["kid"] = center
                stuNameToClassPos[thisStu]["screen"] = (center[0], center[1] - 31)
                stuNameToClassPos[thisStu]["behind"] = (center[0] - 4, center[1] + 40)
                stuNameToClassPos[thisStu]["scale"] = scale
            if orientation == 270:
                stuNameToClassPos[thisStu]["kid"] = center
                stuNameToClassPos[thisStu]["screen"] = (center[0] - 42, center[1])
                stuNameToClassPos[thisStu]["behind"] = (center[0] + 20, center[1] + 16)
                stuNameToClassPos[thisStu]["scale"] = scale
            if orientation == 90:
                stuNameToClassPos[thisStu]["kid"] = center
                stuNameToClassPos[thisStu]["screen"] = (center[0] + 42, center[1])
                stuNameToClassPos[thisStu]["behind"] = (center[0] - 20, center[1] - 16)
                stuNameToClassPos[thisStu]["scale"] = scale
            if orientation == 180:
                stuNameToClassPos[thisStu]["kid"] = center
                stuNameToClassPos[thisStu]["screen"] = (center[0], center[1] + 31)
                stuNameToClassPos[thisStu]["behind"] = (center[0] - 4, center[1] - 40)
                stuNameToClassPos[thisStu]["scale"] = scale

        return stuNameToClassPos

    def load_roster(self):
        rosterPath = askopenfilename(initialdir=os.path.join(dir, 'Class_Rosters'))
        globalParams["classRosterPath"] = rosterPath
        globalParams["classRoster"] = {}

        #open roster and extract all names
        f = open(rosterPath, 'rU')
        reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
        headers = reader.next()
        for row in reader:
            globalParams["classRoster"][row[headers.index("Student_ID")]] = row[headers.index("Anon_ID")]
        self.loadMapButton.configure(state="normal")
        self.createDatasetButton.configure(state="normal")
        self.createMapButton.configure(state="normal")
        self.loadDatasetButton.configure(state="normal")

        vars(self)["roster_label"].configure(text=rosterPath.split("/")[-1])


    def load_existing_map(self):
        dirname = askdirectory(initialdir=os.path.join(dir, 'Saved_Classroom_Maps'))
        imagePath = dirname + "/class_map.gif"
        stuToPosPath = dirname + "/stu_to_position.tsv" 
        if os.path.isfile(imagePath) and os.path.isfile(stuToPosPath):
            globalParams["imagePath"] = imagePath
            globalParams["stuToPosPath"] = stuToPosPath
            vars(self)["map_label"].configure(text=dirname.split("/")[-1])
            globalParams["stuNameToClassPos"] = self.constructStuToPos(globalParams["stuToPosPath"])
        else:
            tkMessageBox.showerror("Invalid input", "Folder must contain both a class_map.png and stu_to_position.tsv file.")

    def load_existing_dataset(self):
        globalParams["mergedDataset"] = askopenfilename(initialdir=os.path.join(dir, 'Saved_Datasets/Merged_Datasets'))
        vars(self)["dataset_label"].configure(text=globalParams["mergedDataset"].split("/")[-1])
        vars(self)["detectorButton"].configure(state="normal")

    def load_detector(self):
        globalParams["detectorName"] = askopenfilename(initialdir=os.path.join(dir, 'Detectors'))
        #try:
        m = __import__ (globalParams["detectorName"].split("/")[-1].split(".")[0])
        func = getattr(m,'runDetector')
        globalParams["detectorAnnotated"], teacherActionSet = func(globalParams["mergedDataset"])
        for action in teacherActionSet:
            valueColorMap[action] = (0,255,0)
        vars(self)["detector_label"].configure(text=globalParams["detectorName"].split("/")[-1])
        self.replaySettingsButton.configure(state="normal")
        #except:
        #    print "\n Invalid detector script. \n\n"

    ### currently assumes only one teacher
    def mergeDatasets(self, datashopName, classObsName):
        datashopLabel = (datashopName.split("/")[-1]).split(".")[0]
        classObsLabel = (classObsName.split("/")[-1]).split(".")[0]
        target_path = os.path.join(dir, 'Saved_Datasets/Merged_Datasets/' + datashopLabel+classObsLabel + '.txt')
        with open(target_path, 'wb') as outputFile:
            f = open(datashopName, 'rU')
            reader = csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE)
            writer = csv.writer(outputFile, delimiter='\t')
            header = next(reader, None)

            ###sort datashop
            sortedList = sorted(reader, key=lambda row: 
                datetime(1900, 1, 1) + (datetime.strptime(row[header.index("CF (tool_event_time)")].split(" ")[1], "%H:%M:%S.%f") - datetime(1900, 1, 1, 4))
                , reverse=False)

            ###read in classroom observations
            classroomObservations = []
            f = open(classObsName, 'rU')
            reader = csv.reader(f)
            startTime = datetime.strptime(reader.next()[0], "%X")
            classObsHeaders = reader.next()
            for row in reader:
                thisObservation = []

                currTimeElapsed = datetime.strptime("00:"+row[0], "%H:%M:%S.%f") - datetime(1900, 1, 1)
                actionStartTime = startTime + currTimeElapsed

                teacherLocation = self.stuNameToDatashopId(row[classObsHeaders.index("Where is teacher")])
                teacherActivity = row[classObsHeaders.index("What is teacher doing")]
                studentsRaisingHand = row[classObsHeaders.index("Students raising hand")]
                if studentsRaisingHand !="":
                    studentsRaisingHand = ",".join(map(self.stuNameToDatashopId, studentsRaisingHand.replace(" ", "").split(",")))

                classroomObservations.append([actionStartTime, teacherLocation, teacherActivity, studentsRaisingHand])

            ###merge datasets
            writer.writerow(header + classObsHeaders[1:] + ["Duration"])
            i=0
            prevTime = ""
            for row in sortedList:
                currTime = row[header.index("CF (tool_event_time)")]
                currTime = datetime.strptime(currTime.split(" ")[1], "%H:%M:%S.%f") - datetime(1900, 1, 1, 4)
                currTime = datetime(1900, 1, 1) + currTime 
                #write row from previous iteration (note: final row from input is currently skipped this way)
                if prevTime!="":
                    rowDuration = (currTime - prevTime).total_seconds()
                    writer.writerow(nextOutput + [rowDuration])
                if i==0:
                    if currTime<classroomObservations[i][0]: #if current time is before the first classroom observation
                        nextOutput = row + classroomObservations[i][1:]
                    else:
                        i+=1
                if i>0:
                    if i>=len(classroomObservations):
                        nextOutput = row + classroomObservations[i-1][1:]
                    else:
                        if currTime<classroomObservations[i][0]:
                            nextOutput = row + classroomObservations[i-1][1:]
                        else:
                            nextOutput = row + classroomObservations[i][1:]
                            i+=1
                prevTime = currTime

        globalParams["mergedDataset"] = target_path

    def create_window_merge(self):
        colorPickerButtons["t"] = tk.Toplevel(self)
        #t.wm_title("Window #%s" % self.counter)
        colorPickerButtons["t"].wm_title("Merge datasets")
        helvInst = tkFont.Font(family='Helvetica', size=13)
        helvHeader = tkFont.Font(family='Helvetica', size=13, weight='bold')
        circleFont = tkFont.Font(family='Helvetica', size=25, weight='bold')


        emptyLabel0 = Tkinter.Label(colorPickerButtons["t"], text="   ")
        emptyLabel0.grid(column=0,row=0,pady=0,padx=0)

        emptyLabel00 = Tkinter.Label(colorPickerButtons["t"], text="       ")
        emptyLabel00.grid(column=1,row=0,pady=10,padx=1)

        #MAP UPLOADS
        map_options = Tkinter.Label(colorPickerButtons["t"], text="Select datasets to merge: ", font=helvHeader)
        map_options.grid(column=1,row=1,pady=10,padx=5)
        self.button = Button(colorPickerButtons["t"], text="Load DataShop dataset", width="30", command=self.load_datashop_dataset)
        self.button.grid(column=2,row=2,pady=2,padx=1)
        self.button = Button(colorPickerButtons["t"], text="Load classroom observations", width="24", command= self.load_classroom_observations)
        self.button.grid(column=3,row=2,pady=2,padx=1)

        emptyLabel01 = Tkinter.Label(colorPickerButtons["t"], text="       ")
        emptyLabel01.grid(column=1,row=4,pady=10,padx=1)


        colorPickerButtons["mergeButton"] = Button(colorPickerButtons["t"], text='Merge', state=DISABLED, font=helvHeader, width=10, command=self.mergeButton)
        colorPickerButtons["mergeButton"].grid(column=7, row=5,pady=10,padx=25)

    def close_replay_windows(self):
        cv2.destroyAllWindows()

    def pause_replay(self):
        if globalParams["pause_flag"] == False:
            globalParams["pause_flag"] = True
        else:
            globalParams["pause_flag"] = False

    def mergeButton(self):
        try:
            self.mergeDatasets(globalParams["datashop_dataset"], globalParams["classroom_observations"])
            vars(self)["dataset_label"].configure(text=globalParams["mergedDataset"].split("/")[-1])
            colorPickerButtons["t"].destroy()
            vars(self)["detectorButton"].configure(state="normal")
        except:
            print "data format error"


    def load_datashop_dataset(self):
        globalParams["datashop_dataset"] = askopenfilename(initialdir=os.path.join(dir, 'Saved_Datasets/DataShop'))
        if globalParams["datashop_dataset"]!="" and globalParams["classroom_observations"]!="":
            colorPickerButtons["mergeButton"].configure(state="normal")

    def load_classroom_observations(self):
        globalParams["classroom_observations"] = askopenfilename(initialdir=os.path.join(dir, 'Saved_Datasets/Classroom_Observations'))
        if globalParams["datashop_dataset"]!="" and globalParams["classroom_observations"]!="":
            colorPickerButtons["mergeButton"].configure(state="normal")

    def create_window_new_map(self):
        globalParams["bgImage"] = askopenfilename(initialdir=os.path.join(dir, 'images'))
        bgImage = globalParams["bgImage"] 
        
        globalParams["nm"] = tk.Toplevel(self)
        globalParams["nm"].wm_title("Create a new map")
        roster = globalParams["classRoster"].keys()
        roster = roster + ["back of class"]
        stuPos = {}

        # create a canvas
        globalParams["nm"].canvas = Canvas(globalParams["nm"], width = 1000, height = 700, bg = 'grey')
        globalParams["nm"].canvas.pack(expand = YES, fill = BOTH)
        image = PhotoImage(file = bgImage)
        self.image = image
        globalParams["nm"].canvas.create_image((0, 0), image = self.image, anchor = NW)

        self._drag_data = {"x": 0, "y": 0, "items": None}
        self._orientation_data = {"items": None}

        width = 100
        height = 50
        paddingTop = 630
        paddingHorizontal = 800
        globalParams["save_button"] = globalParams["nm"].canvas.create_rectangle((paddingHorizontal,paddingTop,
            width+paddingHorizontal, height+paddingTop), outline="black", fill="white", tags="save")
        globalParams["nm"].canvas.create_text(paddingHorizontal+width/2,paddingTop+height/2,text="Save", tags="save")
        (x0,y0,x1,y1)  = globalParams["nm"].canvas.bbox("all")
        width = (x1-x0) + paddingHorizontal
        height = (y1-y0) + paddingTop
        globalParams["nm"].canvas.tag_bind("save", "<ButtonPress-1>", self._on_press)
        globalParams["nm"].canvas.tag_bind("save", "<ButtonRelease-1>", self._on_release)

        for item in roster:
            stuCoords[item] = {"coords": (0,0), "orientation": 0, "scale": 1}
            self._create_token((randint(700,980), randint(100,paddingTop-100)), "green", item)
            if item!="back of class":
                globalParams["nm"].canvas.tag_bind(item, '<Double-Button-1>', self.OnDoubleClick)

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        globalParams["nm"].canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        globalParams["nm"].canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        globalParams["nm"].canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)


    def save_function(self):
        bgImage = globalParams["bgImage"]
        #create/write new map folder
        newMapFolderName = globalParams["classRosterPath"].split(".")[-2].split("/")[-1]
        newpath = os.path.join(dir, "Saved_Classroom_Maps/" + newMapFolderName) 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        #create new files in folder
        oldFileName = bgImage #.split("/")[-1]
        oldFile = bgImage.split("/")[-1]
        newFileName = os.path.join(newpath, "class_map.gif")
        shutil.copy(bgImage, newpath)
        os.rename(newpath + "/" + oldFile, newFileName)
        target_path = newpath + "/" + "stu_to_position.tsv"
        #make new stu position file
        with open (target_path, 'wb') as outputFile:
            writer = csv.writer(outputFile, delimiter='\t')
            writer.writerow(["Student_Name", "Center_Point", "Scale", "Orientation"])
            for item in stuCoords:
                writer.writerow([item, stuCoords[item]["coords"], stuCoords[item]["scale"], stuCoords[item]["orientation"]])
        #save paths
        globalParams["imagePath"] = newFileName
        globalParams["stuToPosPath"] = target_path
        #place this at the end... after path has been acquired
        globalParams["stuNameToClassPos"] = self.constructStuToPos(globalParams["stuToPosPath"])


        vars(self)["map_label"].configure(text=newMapFolderName)

        #close map creator window
        globalParams["nm"].destroy()

    def _on_press(self, event):
        globalParams["nm"].canvas.itemconfig(globalParams["save_button"], fill="grey")

    def _on_release(self, event):
        globalParams["nm"].canvas.itemconfig(globalParams["save_button"], fill="white")
        self.save_function()

    def _create_token(self, coord, color, group_tag):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        if group_tag=="back of class":
            globalParams["nm"].canvas.create_oval(x-10, y-10, x+10, y+10, 
                                    outline=color, fill="grey", tags=("token", group_tag, "kid"))
            i = globalParams["nm"].canvas.create_text(x,y+20,text=group_tag, tags=("token", group_tag, "text"))
            r=globalParams["nm"].canvas.create_rectangle(globalParams["nm"].canvas.bbox(i),fill="white", tags=("token", group_tag, "textbg"))
            globalParams["nm"].canvas.tag_lower(r,i)
        else:
            globalParams["nm"].canvas.create_rectangle(x-25, y-31-15, x+25, y-31+15, fill="black", tags=("token", group_tag, "screen"))
            globalParams["nm"].canvas.create_oval(x-10, y-10, x+10, y+10, 
                                    outline=color, fill=color, tags=("token", group_tag, "kid"))
            i = globalParams["nm"].canvas.create_text(x,y+20,text=group_tag, tags=("token", group_tag, "text"))
            r=globalParams["nm"].canvas.create_rectangle(globalParams["nm"].canvas.bbox(i),fill="white", tags=("token", group_tag, "textbg"))
            globalParams["nm"].canvas.tag_lower(r,i)
            globalParams["nm"].canvas.create_oval(x-4-9, y-9+40, x-4+9, y+9+40, 
                                    outline=color, fill="grey", tags=("token", group_tag, "teacher"))

    def OnDoubleClick(self, event):
        self._orientation_data["items"] = globalParams["nm"].canvas.find_withtag(globalParams["nm"].canvas.gettags( globalParams["nm"].canvas.find_closest(event.x, event.y)[0] )[1])
        stuName = globalParams["nm"].canvas.gettags(self._orientation_data["items"][0])[1]
        if stuCoords[stuName]["orientation"] == 270:
            stuCoords[stuName]["orientation"] = 0
        else:
            stuCoords[stuName]["orientation"] += 90

        screen = set(globalParams["nm"].canvas.find_withtag("screen")).intersection(set(self._orientation_data["items"])).pop()
        teacher = set(globalParams["nm"].canvas.find_withtag("teacher")).intersection(set(self._orientation_data["items"])).pop()
        kid = set(globalParams["nm"].canvas.find_withtag("kid")).intersection(set(self._orientation_data["items"])).pop()
        text = set(globalParams["nm"].canvas.find_withtag("text")).intersection(set(self._orientation_data["items"])).pop()
        textbg = set(globalParams["nm"].canvas.find_withtag("textbg")).intersection(set(self._orientation_data["items"])).pop()
        kidCoords = globalParams["nm"].canvas.coords(kid)
        x = (kidCoords[0]+kidCoords[2])/2
        y = (kidCoords[1]+kidCoords[3])/2
        print stuCoords[stuName]["orientation"]
        if stuCoords[stuName]["orientation"] == 0:
            globalParams["nm"].canvas.coords(screen, (x-25, y-31-15, x+25, y-31+15))
            globalParams["nm"].canvas.coords(teacher, (x-4-9, y+40-9, x-4+9, y+40+9))
            globalParams["nm"].canvas.coords(text, (x,y+20))
            globalParams["nm"].canvas.coords(textbg, globalParams["nm"].canvas.bbox(text))
        if stuCoords[stuName]["orientation"] == 90:
            globalParams["nm"].canvas.coords(screen, (x+42-25, y-15, x+42+25, y+15))
            globalParams["nm"].canvas.coords(teacher, (x-20-9, y-16-9, x-20+9, y-16+9))
            globalParams["nm"].canvas.coords(text, (x-40,y+10))
            globalParams["nm"].canvas.coords(textbg, globalParams["nm"].canvas.bbox(text))
        if stuCoords[stuName]["orientation"] == 180:
            globalParams["nm"].canvas.coords(screen, (x-25, y+31-15, x+25, y+31+15))
            globalParams["nm"].canvas.coords(teacher, (x-4-9, y-40-9, x-4+9, y-40+9))
            globalParams["nm"].canvas.coords(text, (x,y-20))
            globalParams["nm"].canvas.coords(textbg, globalParams["nm"].canvas.bbox(text))
        if stuCoords[stuName]["orientation"] == 270:
            globalParams["nm"].canvas.coords(screen, (x-42-25, y-15, x-42+25, y+15))
            globalParams["nm"].canvas.coords(teacher, (x+20-9, y+16-9, x+20+9, y+16+9))
            globalParams["nm"].canvas.coords(text, (x+40,y))
            globalParams["nm"].canvas.coords(textbg, globalParams["nm"].canvas.bbox(text))

    def OnTokenButtonPress(self, event):
        '''Begin drag of an object'''
        # record the item and its location
        self._drag_data["items"] = globalParams["nm"].canvas.find_withtag(globalParams["nm"].canvas.gettags( globalParams["nm"].canvas.find_closest(event.x, event.y)[0] )[1])
        #print self._drag_data["items"]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        if self._drag_data["items"]!=None:
            #update position data
            stuName = globalParams["nm"].canvas.gettags(self._drag_data["items"][0])[1]
            kid = set(globalParams["nm"].canvas.find_withtag("kid")).intersection(set(self._drag_data["items"])).pop()
            kidCoords = globalParams["nm"].canvas.coords(kid)
            kidX = (kidCoords[0]+kidCoords[2])/2
            kidY = (kidCoords[1]+kidCoords[3])/2
            stuCoords[stuName]["coords"] = (kidX, kidY)
            # reset the drag information
            self._drag_data["items"] = None
            self._drag_data["x"] = 0
            self._drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the objects the appropriate amount
        for item in self._drag_data["items"]:
            globalParams["nm"].canvas.move(item, delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def gen_hex_colour_code(self):
        return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

    def gen_tuple(self, rgb):
        return "".join(map(chr, rgb)).encode('hex')

    def create_window_replay_settings(self):
        
        rs = tk.Toplevel(self)
        rs.wm_title("Replay settings")

        self.replayButton.configure(state="normal")

        helvInst = tkFont.Font(family='Helvetica', size=13)
        helvHeader = tkFont.Font(family='Helvetica', size=13, weight='bold')
        circleFont = tkFont.Font(family='Helvetica', size=25, weight='bold')

        values = valueColorMap.keys()
        raisedHandColor = defaultParameters["raisedHandColor"]
        colorStart = defaultParameters["colorStart"]
        colorEnd = defaultParameters["colorEnd"]
        defaultColor = defaultParameters["defaultColor"]
        minValue = defaultParameters["minValue"] #the min endpoint of the color spectrum
        maxValue = defaultParameters["maxValue"]  #the max endpoint of the color spectrum
        playbackSpeed = defaultParameters["playbackSpeed"]
        refreshRate = defaultParameters["refreshRate"]


        #HEADER
        headerInstructions = Tkinter.Label(rs, text="Select a display color for each variable level below:", wraplength=160, justify="center", font=helvInst)
        headerInstructions.grid(column=2,row=0,pady=10,padx=1)
        emptyLabel00 = Tkinter.Label(rs, text="       ")
        emptyLabel00.grid(column=2,row=0,pady=1,padx=1)
        headerTeacherVars = Tkinter.Label(rs, text="Teacher variable (colors)", font=helvHeader)
        headerTeacherVars.grid(column=2,row=2,pady=5,padx=1)

        headerInstructions2 = Tkinter.Label(rs, text="Set the playback parameters below:", font=helvInst)
        headerInstructions2.grid(column=5,row=0,pady=1,padx=1)
        emptyLabel01 = Tkinter.Label(rs, text="       ")
        emptyLabel01.grid(column=5,row=1,pady=1,padx=1)
        playbackParamLabel = Tkinter.Label(rs, text="Playback parameters", font=helvHeader)
        playbackParamLabel.grid(column=5,row=2,pady=1,padx=1)
        
        for item in range(0,len(values)):
            hexstr = self.gen_hex_colour_code() #random color initialization
            valueColorMap[values[item]] = tuple(ord(c) for c in hexstr.decode('hex'))
            rs.button = Button(rs, text=values[item], command=lambda x=item: self.colourer('label'+'_'+str(x)), justify="center", width="24")
            colorPickerButtons['label'+'_'+str(item)]= Tkinter.Label(rs, text=u'\u2B24', fg="#"+hexstr, font=circleFont)
            colorPickerButtons['label'+'_'+str(item)].grid(column=1,row=item+4,pady=5,padx=1)
            rs.button.grid(column=2,row=item+4,pady=5,padx=0)

        #sliders (min, max, playback speed, refresh rate)
        w = Tkinter.Scale(rs, from_=100, to=9000, orient=HORIZONTAL, length=150, sliderlength=10, resolution=2, command=lambda x: self.set_slider_value(x, "playbackSpeed"))
        w.grid(column=5, row=4)
        w.set(playbackSpeed)
        wLabel = Tkinter.Label(rs, text="Replay speed", font=helvHeader)
        wLabel.grid(column=5, row=5,pady=5)

        w2 = Tkinter.Scale(rs, from_=1, to=100, orient=HORIZONTAL, length=150, sliderlength=10, command=lambda x: self.set_slider_value(x, "refreshRate"))
        w2.grid(column=6, row=4, pady=1)
        w2.set(refreshRate)
        w2Label = Tkinter.Label(rs, text="Refresh rate", font=helvHeader)
        w2Label.grid(column=6, row=5,pady=5)

        headerDetectorParameters = Tkinter.Label(rs, text="Detector parameters", font=helvHeader, justify="right")
        headerDetectorParameters.grid(column=5,row=item+9,pady=14,padx=10)

        w3 = Tkinter.Scale(rs, from_=0, to=300, orient=HORIZONTAL, length=150, sliderlength=10, command=lambda x: self.set_slider_value(x, "minValue"))
        w3.grid(column=5, row=item+11)
        w3.set(minValue)
        w3Label = Tkinter.Label(rs, text="Min. detector value", font=helvHeader)
        w3Label.grid(column=5, row=item+12,pady=5)

        w4 = Tkinter.Scale(rs, from_=0, to=300, orient=HORIZONTAL, length=150, sliderlength=10, command=lambda x: self.set_slider_value(x, "maxValue"))
        w4.grid(column=6, row=item+11, pady=1)
        w4.set(maxValue)
        w4Label = Tkinter.Label(rs, text="Max. detector value", font=helvHeader)
        w4Label.grid(column=6, row=item+12, pady=5)

        #HEADER
        emptyLabel0 = Tkinter.Label(rs, text="       ")
        emptyLabel0.grid(column=2,row=item+5,pady=1,padx=10)
        headerStudentVars = Tkinter.Label(rs, text="Student indicator (colors)", font=helvHeader)
        headerStudentVars.grid(column=2,row=item+6,pady=0,padx=10)

        #Raising hand color
        rs.button = Button(rs, text="Student raising hand", width="24", command=lambda x=item+1: self.colourer('label'+'_'+'raisedHandColor'))
        colorPickerButtons['label'+'_'+'raisedHandColor']= Tkinter.Label(rs, text=u'\u2B24', fg="#"+self.gen_tuple(raisedHandColor), font=circleFont)
        colorPickerButtons['label'+'_'+'raisedHandColor'].grid(column=1,row=item+7,pady=2,padx=10)
        rs.button.grid(column=2,row=item+7,pady=2,padx=1)

        #HEADER
        emptyLabel1 = Tkinter.Label(rs, text="       ")
        emptyLabel1.grid(column=2,row=item+8,pady=1,padx=4)
        headerDetectorVars = Tkinter.Label(rs, text="Detector variable (colors)", font=helvHeader)
        headerDetectorVars.grid(column=2,row=item+9,pady=4,padx=10)

        #Min color
        rs.button = Button(rs, text="Min. detector value color", width="24",  command=lambda x=item+1: self.colourer('label'+'_'+'colorStart'))
        colorPickerButtons['label'+'_'+'colorStart']= Tkinter.Label(rs, text="       ", bg="#"+self.gen_tuple(colorStart))
        colorPickerButtons['label'+'_'+'colorStart'].grid(column=1,row=item+11,pady=5,padx=10)
        rs.button.grid(column=2,row=item+11,pady=5,padx=1)

        #Max color
        rs.button = Button(rs, text="Max. detector value color", width="24", command=lambda x=item+1: self.colourer('label'+'_'+'colorEnd'))
        colorPickerButtons['label'+'_'+'colorEnd']= Tkinter.Label(rs, text="       ", bg="#"+self.gen_tuple(colorEnd))
        colorPickerButtons['label'+'_'+'colorEnd'].grid(column=1,row=item+12,pady=5,padx=10)
        rs.button.grid(column=2,row=item+12,pady=5,padx=1)

        #Default color
        rs.button = Button(rs, text="Student not yet started", width="24",  command=lambda x=item+1: self.colourer('label'+'_'+'defaultColor'))
        colorPickerButtons['label'+'_'+'defaultColor']= Tkinter.Label(rs, text="       ", bg="#"+self.gen_tuple(defaultColor))
        colorPickerButtons['label'+'_'+'defaultColor'].grid(column=1,row=item+13,pady=5,padx=10)
        rs.button.grid(column=2,row=item+13,pady=5,padx=1)

        emptyLabel3 = Tkinter.Label(rs, text="       ")
        emptyLabel3.grid(column=3,row=item+14,pady=10,padx=10)

        rs.quitButton = Button(rs, text='Done', font=helvHeader, width=10, command=rs.destroy)
        rs.quitButton.grid(column=7, row=item+15,pady=10,padx=25)


    def colourer(self, labelName):
        result = askcolor()
        result_tuple = tuple(reversed(result[0]))
        result_hex = result[1]
        label_extract = labelName.split('_')[-1]
        values = valueColorMap.keys()
        if label_extract in defaultParameters.keys() and label_extract!="raisedHandColor":
            colorPickerButtons[labelName].configure(bg=result_hex)
        else:
            colorPickerButtons[labelName].configure(fg=result_hex)

        if label_extract not in defaultParameters.keys():
            valueColorMap[values[int(labelName.split('_')[-1])]] = result_tuple
        else:
            defaultParameters[labelName.split('_')[-1]] = result_tuple

    def set_slider_value(self, val, paramName):
        defaultParameters[paramName] = float(val)


    def create_window_replay(self):
        stuNameToClassPos = globalParams["stuNameToClassPos"]
        values = valueColorMap.keys()
        raisedHandColor = defaultParameters["raisedHandColor"]
        colorStart = defaultParameters["colorStart"]
        colorEnd = defaultParameters["colorEnd"]
        defaultColor = defaultParameters["defaultColor"]
        minValue = defaultParameters["minValue"] #the min endpoint of the color spectrum
        maxValue = defaultParameters["maxValue"]  #the max endpoint of the color spectrum
        playbackSpeed = defaultParameters["playbackSpeed"]
        refreshRate = defaultParameters["refreshRate"]

        teacher_radius = 10; lineThickness = -1
        playbackProportion = 1./playbackSpeed
        colorDiff = tuple(np.subtract(colorEnd, colorStart))
        stuColors = {}

        for stuName in stuNameToClassPos.keys():
            if stuName!="back of class":
                stuColors[stuName] = defaultColor

        if True:
            cv2.WINDOW_NORMAL

            #gif to png conversion necessary for opencv
            filepath,filename = os.path.split(globalParams["imagePath"])
            filterame,exts = os.path.splitext(filename)
            im = Image.open(globalParams["imagePath"])
            newImgFile = os.path.join(filepath, filterame+'.png')
            im.save(newImgFile,'PNG')

            # #find and display background image for classSessionName
            baseImg = cv2.imread(newImgFile, cv2.IMREAD_COLOR)
            img = copy.deepcopy(baseImg)

            f = open(globalParams["detectorAnnotated"], 'rU')
            reader = csv.reader(f, delimiter='\t',quoting=csv.QUOTE_NONE)
            headers = reader.next()

            teacher_position_ind = headers.index("Where is teacher"); 
            teacher_action_ind = headers.index("What is teacher doing")
            row_duration_ind = headers.index("Duration")
            raised_hand_ind = headers.index("Students raising hand")


            counter=0
            for row in reader:
                if globalParams["pause_flag"]==True:
                    #get row variables...
                    teacher_position = row[teacher_position_ind]
                    teacher_action = row[teacher_action_ind]
                    class_state = eval(row[headers.index("classState")])
                    raisedHand = row[raised_hand_ind]
                    if row[row_duration_ind] == "":
                        break
                    else:
                        row_duration = float(row[row_duration_ind])

                    #draw and hold for playbackProportion*row_duration seconds
                    counter+=1
                    #print teacher_position, "   ", teacher_action, "      ", counter 
                    if counter%refreshRate==0:
                        img = copy.deepcopy(baseImg)

                        if teacher_position!="back of class":
                            #print IDToStu[teacher_position], teacher_position
                            teacher_position = teacher_position.split()[0]
                            teacher_xy = stuNameToClassPos[IDToStu[teacher_position]]["behind"]
                        else:
                            teacher_xy = stuNameToClassPos["back of class"]["behind"]

                        #update teacher display
                        circle_color = valueColorMap[teacher_action] 
                        cv2.circle(img, teacher_xy, teacher_radius, circle_color, lineThickness)

                        #update all student state displays
                        for item in stuColors.keys():
                            stuID = self.stuNameToDatashopId(item)
                            if stuID in class_state.keys():
                                currValue = float(class_state[stuID])

                                if currValue < minValue:
                                    stuColors[item] = colorStart
                                else:
                                    stuColors[item] = np.add(colorStart, np.multiply((currValue/maxValue), colorDiff))

                            classPos = stuNameToClassPos[item]

                            cv2.rectangle(img, tuple(np.subtract(classPos["screen"], (25,15))), tuple(np.subtract(classPos["screen"], (-25,-15))), stuColors[item], -1)

                            if stuID == raisedHand.split(" ")[0]:
                                cv2.circle(img, classPos["kid"], 9, raisedHandColor, -1)
                        
                        cv2.imshow('SPACLE',img)
                        cv2.waitKey(1)

                    sleep(playbackProportion*row_duration)

        

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SPACLE')
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()