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

# Dummy data initialize to empty list '[]' later
elementsToDisplay = ["K", "Ca", "Au"]
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

        # Add the test parse button across bottom of both columns
        # nextButton = QPushButton("Test File Parsing")
        # nextButton.clicked.connect(self.makeInputFileIdeal)
        # layout.addWidget(nextButton, 3, 0, 1, 2)

        layout.setVerticalSpacing(10)
        self.setLayout(layout)

    # If "add" item is clicked in XRF input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def XRFClicked(self, qmodelindex):
        if(self.XRFInput.currentItem().text() == "Add an XRF file"):
            dialog = QFileDialog
            res = dialog.getOpenFileName(self, 'Open file', '',"XRF files (*.csv)")
            if(res[0]):
                duplicate = 0
                for i in range(self.XRFInput.count()):
                    if(res[0] == self.XRFInput.item(i).text()):
                        duplicate = 1
                if not duplicate:
                    if self.isFileValid("XRF", res[0]):
                        self.XRFInput.insertItem(1, res[0])
                        self.addToDictMaster(res[0])
                        self.makeInputFileIdeal(res[0])
        else:
            app.dictMaster.pop(self.XRFInput.currentItem().text())
            self.XRFInput.takeItem(self.XRFInput.currentRow())
            print("Removed Item from Dict Master",app.dictMaster)

        self.XRFInput.clearSelection()

    # If "add" item is clicked in Concentration input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def ConClicked(self, qmodelindex):
        if(self.conInput.currentItem().text() == "Add a Concentration file"):
            dialog = QFileDialog
            res = dialog.getOpenFileName(self, 'Open file', '',"Calibration files (*.csv)")
            if(res[0]):
                duplicate = 0
                for i in range(self.conInput.count()):
                    if(res[0] == self.conInput.item(i).text()):
                        duplicate = 1
                if not duplicate:
                    if self.isFileValid("Concentration", res[0]):
                        self.conInput.insertItem(1, res[0])
                        self.addToConDict(res[0])
                        #self.makeInputFileIdeal(res[0])
        else:
            app.conDict.pop(self.conInput.currentItem().text())
            self.conInput.takeItem(self.conInput.currentRow())
            print("Removed Item from conDict",app.conDict)
        self.conInput.clearSelection()


    def createFileErrorMsgBox(self, missingFields):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Update the file to include the headers listed below:")
        msg.setInformativeText(', '.join(missingFields))
        msg.setWindowTitle("Error: Missing Values")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def unifyHeaderNames(self, columns):
        #replace some variations on important names
        if("Core Type" in columns):
            columns[columns.index("Core Type")] = "Type"
        for header in columns:
            if("Interval" in header):
                columns[columns.index(header)] = "Interval"
                break

        return columns

    def isFileValid(self, key, filename):
        valid = True
        print("check if file has info we need")
        missingFields = []
        neededData = ["Site","Hole","Core", "Type","Section","Interval"]

        print("File: ", filename)
        file = open(filename , 'r')
        reader = csv.DictReader(file)
        dict_from_csv = dict(list(reader)[0])
        columns = list(dict_from_csv.keys())
        columns = self.unifyHeaderNames(columns)
        #print("Columns ", columns)

        #does it have all the data we need? what data is it missing?
        for i in neededData:
            if(not (i in columns)):
                missingFields.append(i)

        #Were they missing something?
        if(len(missingFields)>0):
            valid = False

        if(not valid):
            self.createFileErrorMsgBox(missingFields)
        else:
            return 1
        return 0

    def addToDictMaster(self, fname):
        app.dictMaster[fname] = {}
        neededData = ["Site","Hole","Core","Section"]
        #check for near match of interval and core type

        vals = self.isHeaderInFile("Type",fname)
        if(vals!="null"):
            neededData.append(vals)
        vals = self.isHeaderInFile("Interval",fname)
        if(vals!="null"):
            neededData.append(vals)
        print(neededData)

        file = pd.read_csv(fname, usecols = neededData)
        app.dictMaster[fname] = file.to_dict(orient='list')
        print("\n\n\n\nHayden Dict: ", app.dictMaster)
        # print(file)

    def addToConDict(self, fname):
        app.conDict[fname] = {}
        neededData = ["Site","Hole","Core","Section"]

        #check for near match of interval and core type
        vals = self.isHeaderInFile("Type",fname)
        if(vals!="null"):
            neededData.append(vals)

        vals = self.isHeaderInFile("Interval",fname)
        if(vals!="null"):
            neededData.append(vals)
        #print(neededData)

        file = pd.read_csv(fname, usecols = neededData)
        app.conDict[fname] = file.to_dict(orient='list')
        print("\n\n\n\nHayden conDict: ", app.conDict)

        count = 0
        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, fname)
            #print(temp)
            if temp[0]:
                df = pd.read_csv(fname, usecols = [temp[1]])
                app.conDict[fname].update(df.to_dict(orient='list'))
                app.conDict[fname][element] = app.conDict[fname].pop(temp[0])
        print("\n\n\n\nTommy conDict: ", app.conDict)

    def isHeaderInFile(self, key, fileName):
        file = open(fileName ,'r')
        reader = csv.reader(file)
        headerRow = list(reader)[0]
        for header in headerRow:
            if(key in header):
                return header
        return "null"

    def msgbtn(self, i):
        if(i.text()=="Retry"):
            print("Enter Info")

        print("Button pressed: " + i.text())

    # goes through list of elements, so will not check for multiple headers with same beginning element in name
    def makeInputFileIdeal(self, filename):
        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, filename)
            if temp[0]:
                df = pd.read_csv(filename, usecols = [temp[1]])
                app.dictMaster[filename].update(df.to_dict(orient='list'))
                app.dictMaster[filename][element] = app.dictMaster[filename].pop(temp[0])

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
