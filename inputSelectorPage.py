import sys
import random
import csv
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint
from elements import *
import pandas as pd
import re
import app

#concentration elements
elementsToDisplay = []
#XRF elements
xrfElements = []
# **IMPORTANT** When the time comes to populate this list with acutal data you
# must have the line "global elementsToDisplay" in the local scope before
# populating the list. Otherwise a new variable will be created in that scope with
# the same name and the data will not be transfered between pages.

class InputSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(InputSelectorPage,self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Initialize window with format
        layout = QGridLayout(self)

        # Create first column header and add to layout
        labelOne = QLabel("Add an XRF file or click to remove:")
        labelOne.setAlignment(Qt.AlignHCenter)
        layout.addWidget(labelOne, 0, 0)

        # Create second column header and add to layout
        labelTwo = QLabel("Add a Concentration file or click to remove:")
        labelTwo.setAlignment(Qt.AlignHCenter)
        layout.addWidget(labelTwo, 0, 1)

        # Create XRF list widget and add to the first column
        self.XRFInput = QListWidget()
        self.XRFInput.setSelectionMode(QAbstractItemView.SingleSelection)
        self.XRFInput.insertItem(0, "Add an XRF file")
        self.XRFInput.clicked.connect(self.XRFClicked)
        layout.addWidget(self.XRFInput, 1, 0)

        # Create Calibration list widget and add to the second column
        self.conInput = QListWidget()
        self.conInput.setSelectionMode(QAbstractItemView.SingleSelection)
        self.conInput.insertItem(0, "Add a Concentration file")
        self.conInput.clicked.connect(self.ConClicked)
        layout.addWidget(self.conInput, 1, 1)

        layout.setVerticalSpacing(10)
        self.setLayout(layout)


    #reset elementsToDisplay when creating the page
    def initializePage(self):
        global elementsToDisplay
        elementsToDisplay = []

    # If "add" item is clicked in XRF input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def XRFClicked(self, qmodelindex):
        if(self.XRFInput.currentItem().text() == "Add an XRF file"):
            dialog = QFileDialog
            res = dialog.getOpenFileNames(self, 'Open file', '',"XRF files (*.csv)")
            if(res[0]):
                for file in res[0]:
                    duplicate = 0
                    for i in range(self.XRFInput.count()):
                        if(file == self.XRFInput.item(i).text()):
                            duplicate = 1
                    if not duplicate:
                        if self.isFileValid("XRF", file):
                            self.XRFInput.insertItem(1, file)
                            self.addToDictMaster(file)
        else:
            app.dictMaster.pop(self.XRFInput.currentItem().text())
            self.XRFInput.takeItem(self.XRFInput.currentRow())
        self.XRFInput.clearSelection()
        #print(app.dictMaster)
        self.completeChanged.emit()

    # If "add" item is clicked in Concentration input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def ConClicked(self, qmodelindex):
        if(self.conInput.currentItem().text() == "Add a Concentration file"):
            dialog = QFileDialog
            res = dialog.getOpenFileNames(self, 'Open file', '',"Calibration files (*.csv)")
            if(res[0]):
                for file in res[0]:
                    duplicate = 0
                    if(self.conInput.count()>1):
                        self.createTooManyConcentrationMsgBox()
                    #for i in range(self.conInput.count()):
                        #if(file == self.conInput.item(i).text()):
                            #duplicate = 1
                    #if not duplicate:
                    else:
                        if self.isFileValid("Concentration", file):
                            self.conInput.insertItem(1, file)
                            self.addToConDict(file)
        else:
            app.conDict.pop(self.conInput.currentItem().text())
            self.conInput.takeItem(self.conInput.currentRow())
            global elementsToDisplay
            elementsToDisplay = []
        self.conInput.clearSelection()
        self.completeChanged.emit()

    def createTooManyConcentrationMsgBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You may only upload 1 concentration file at a time.")
        msg.setWindowTitle("Error: Too Many Files")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.exec_()

    #generates the message box that tells the user to upload valid files
    def createFileErrorMsgBox(self, missingFields, cols):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        add = "Found the Following Column Headers:\n" + ', '.join(cols) + "\n\nNeeded Columns That are Missing:\n" + ', '.join(missingFields)
        msg.setText(add)
        #msg.setInformativeText(', '.join(missingFields))
        msg.setWindowTitle("Error: Missing Values")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    #deals with issue regarding Type v Core Type and Interval v Interval (cm)
    def unifyHeaderNames(self, columns):
        #replace some variations on important names
        if("Core Type" in columns):
            columns[columns.index("Core Type")] = "Type"
        for header in columns:
            if("Interval" in header):
                columns[columns.index(header)] = "Interval"
                break

        return columns

    #determines if an uploaded file has the required Site, Hole, Core, Type, Section, and Interval data
    def isFileValid(self, key, filename):
        valid = True
        missingFields = []
        neededData = ["Site","Hole","Core", "Type","Section","Interval"]

        #get all headers from the uploaded file
        file = open(filename , 'r')
        reader = csv.DictReader(file)
        dict_from_csv = dict(list(reader)[0])
        columns = list(dict_from_csv.keys())
        #columns = self.unifyHeaderNames(columns)


        #does it have all the data we need? what data is it missing?
        for i in neededData:
            if(not (i in columns)):
                missingFields.append(i)

        #Were they missing something?
        if(len(missingFields)>0):
            valid = False

        if(not valid):
            self.createFileErrorMsgBox(missingFields, columns)
        else:
            return 1
        return 0

    #add retrieved data to the dictionary containing all XRF data
    def addToDictMaster(self, fname):
        #create the dictionary for this file
        app.dictMaster[fname] = {}
        #used to find these columns from XRF file and init the dictionary for this file
        neededData = ["Site","Hole","Core","Section"]

        #check for near match of interval and core type
        vals = self.isHeaderInFile("Type",fname)

        if(vals!="null"):
            neededData.append(vals)
        vals = self.isHeaderInFile("Interval",fname)
        if(vals!="null"):
            neededData.append("Interval")

        #create the dictionary with neededData columns from above
        file = pd.read_csv(fname, usecols = neededData)
        app.dictMaster[fname] = file.to_dict(orient='list')

        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, fname)
            if temp[0]:
                global xrfElements
                xrfElements.append(element)

                df = pd.read_csv(fname, usecols = [temp[1]])
                app.dictMaster[fname].update(df.to_dict(orient='list'))
                app.dictMaster[fname][element] = app.dictMaster[fname].pop(temp[0])
        self.removeNonNumericDictMasterData()

    #add retrieved data to the dictionary containing all Concentration data
    def addToConDict(self, fname):
        #create the dictionary for this file
        app.conDict[fname] = {}
        #used to find these columns from XRF file and init the dictionary for this file
        neededData = ["Site","Hole","Core","Section"]

        #check for near match of interval and core type
        vals = self.isHeaderInFile("Type",fname)
        if(vals!="null"):
            neededData.append(vals)
        vals = self.isHeaderInFile("Interval",fname)
        if(vals!="null"):
            neededData.append("Interval")

        #create the dictionary with neededData columns from above
        file = pd.read_csv(fname, usecols = neededData)
        app.conDict[fname] = file.to_dict(orient='list')
        count = 0
        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, fname)
            if temp[0]:
                #ElementSelectorPage.conElements.append(temp[0])
                #update the element selector screen
                global elementsToDisplay
                elementsToDisplay.append(temp[0])
                #add to the concentration dictionary the data collected from this file
                df = pd.read_csv(fname, usecols = [temp[1]])
                app.conDict[fname].update(df.to_dict(orient='list'))
                app.conDict[fname][element] = app.conDict[fname].pop(temp[0])
        self.removeNonNumericConDictData()

    #parse through every element in each file of conDict and replace all non numeric input with the int equivalent or zero
    def removeNonNumericConDictData(self):
        #all files in conDict
        for file in app.conDict:
            #all column headers in the file dictionary
            for key in app.conDict[file]:
                #if the header is an element
                if(key in elements):
                    #loop through the values
                    for i in range(0,len(app.conDict[file][key])):
                        #if the value is a string
                        if(isinstance(app.conDict[file][key][i],str)):
                            #see if the string can be parsed directly into an int
                            try:
                                app.conDict[file][key][i] = int(app.conDict[file][key][i])
                            #string is not a number so we make it zero
                            except ValueError:
                                app.conDict[file][key][i] = 0


    #parse through every element in each file of dictMaster and replace all non numeric input with the int equivalent or zero
    def removeNonNumericDictMasterData(self):
        #all files in conDict
        for file in app.dictMaster:
            #all column headers in the file dictionary
            for key in app.dictMaster[file]:
                #if the header is an element
                if(key in elements):
                    #loop through the values
                    for i in range(0,len(app.dictMaster[file][key])):
                        #if the value is a string
                        if(isinstance(app.dictMaster[file][key][i],str)):
                            #print("Found string: "+ app.dictMaster[file][key][i])
                            #see if the string can be parsed directly into an int
                            try:
                                app.dictMaster[file][key][i] = int(app.dictMaster[file][key][i])
                            #string is not a number so we make it zero
                            except ValueError:
                                app.dictMaster[file][key][i] = 0


    #given a header (key) and filename, this will determine if it exists in the file, null otherwise
    def isHeaderInFile(self, key, fileName):
        file = open(fileName ,'r')
        reader = csv.reader(file)
        headerRow = list(reader)[0]
        for header in headerRow:
            if(key in header):
                return header
        return "null"

    #unused button function
    def msgbtn(self, i):
        print("Button pressed: " + i.text())

    #given an element (Fe) and filename, will determine if a column header contains that element with some regex to handle different string literals
    def isElementInFile(self, element, fileName):
        file = open(fileName ,'r')
        reader = csv.reader(file)
        headerRow = next(reader)
        for index, header in enumerate(headerRow):
            if "std" not in header.lower():
                if re.search(element+'([0-9]|-|_|\s).*', header.strip()[:3]):
                    file.close()
                    return header, index
                if header == element:
                    file.close()
                    return header, index
        file.close()
        return None, -1

    def isComplete(self):
        return self.XRFInput.item(1) is not None and self.conInput.item(1) is not None
