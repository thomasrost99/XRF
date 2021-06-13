import csv
from PyQt5 import QtWidgets, QtCore
from elements import elements
import pandas as pd
import re
import app

# concentration elements
elementsToDisplay = []
# XRF elements
xrfElements = []
# **IMPORTANT** When the time comes to populate this list with acutal data you
# must have the line "global elementsToDisplay" in the local scope before
# populating the list. Otherwise a new variable will be created in that scope with
# the same name and the data will not be transfered between pages.


class InputSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(InputSelectorPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Initialize window with format
        layout = QtWidgets.QGridLayout(self)

        # Create first column header and add to layout
        labelOne = QtWidgets.QLabel("Add an XRF file or click to remove:")
        labelOne.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(labelOne, 0, 0)

        # Create second column header and add to layout
        labelTwo = QtWidgets.QLabel(
            "Add a Concentration file or click to remove:")
        labelTwo.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(labelTwo, 0, 1)

        # Create XRF list widget and add to the first column
        self.XRFInput = QtWidgets.QListWidget()
        self.XRFInput.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.XRFInput.insertItem(0, "Add an XRF file")
        self.XRFInput.clicked.connect(self.XRFClicked)
        layout.addWidget(self.XRFInput, 1, 0)

        # Create Calibration list widget and add to the second column
        self.conInput = QtWidgets.QListWidget()
        self.conInput.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.conInput.insertItem(0, "Add a Concentration file")
        self.conInput.clicked.connect(self.ConClicked)
        layout.addWidget(self.conInput, 1, 1)

        layout.setVerticalSpacing(10)
        self.setLayout(layout)

    # reset elementsToDisplay when creating the page

    def initializePage(self):
        global elementsToDisplay
        elementsToDisplay = []
        global xrfElements
        xrfElements = []

    # If "add" item is clicked in XRF input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def XRFClicked(self, qmodelindex):
        # if they click add file open a file selector looking for csv files only
        if(self.XRFInput.currentItem().text() == "Add an XRF file"):
            dialog = QtWidgets.QFileDialog
            res = dialog.getOpenFileNames(
                self, 'Open file', '', "XRF files (*.csv)")

            # was a file selected
            if(res[0]):
                for file in res[0]:
                    duplicate = 0
                    for i in range(self.XRFInput.count()):
                        # see if this file is already in the list
                        if(file == self.XRFInput.item(i).text()):
                            duplicate = 1
                    # if this was a new file not already present, add it to the list and populate the dictMaster (XRF dictionary)
                    if not duplicate:
                        # check for neccesary headers
                        if self.isFileValid("XRF", file):
                            self.XRFInput.insertItem(1, file)
                            self.addToDictMaster(file)
        # if a file was clicked, remove it from the list and update dictionaries
        else:
            app.dictMaster.pop(self.XRFInput.currentItem().text())
            self.XRFInput.takeItem(self.XRFInput.currentRow())
        # notify changes and clear selection stack
        self.XRFInput.clearSelection()
        self.completeChanged.emit()

    # If "add" item is clicked in Concentration input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def ConClicked(self, qmodelindex):
        # if they click add file open a file selector looking for csv files only
        if(self.conInput.currentItem().text() == "Add a Concentration file"):
            dialog = QtWidgets.QFileDialog
            res = dialog.getOpenFileNames(
                self, 'Open file', '', "Calibration files (*.csv)")
            # if a file was selected
            if(res[0]):
                for file in res[0]:
                    duplicate = 0
                    # if there is more than one concentration file presentr in the list spawn error box (LIMIT 1)
                    if(self.conInput.count() > 1):
                        self.createTooManyConcentrationMsgBox()
                    # if there is not a concentration file uplaoded yet, add the selected one and update the concentration dictionary
                    else:
                        # see if it has the neccesary headers
                        if self.isFileValid("Concentration", file):
                            self.conInput.insertItem(1, file)
                            self.addToConDict(file)
        # if they clicked a file already in the list, remove it from the dicitionaries
        else:
            app.conDict.pop(self.conInput.currentItem().text())
            self.conInput.takeItem(self.conInput.currentRow())
            # there will be no elements on the following screen until a concentration file is selected
            global elementsToDisplay
            elementsToDisplay = []
        # notify the app of changes to the concentration list
        self.conInput.clearSelection()
        self.completeChanged.emit()

    # message box that appears when the user tries to upload more than 1 concention file (LIMIT 1)
    def createTooManyConcentrationMsgBox(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("You may only upload 1 concentration file at a time.")
        msg.setWindowTitle("Error: Too Many Files")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    # generates the message box that tells the user to upload valid files
    def createFileErrorMsgBox(self, missingFields, cols):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        add = "Found the Following Column Headers:\n" + \
            ', '.join(cols) + "\n\nNeeded Columns That are Missing:\n" + \
            ', '.join(missingFields)
        msg.setText(add)
        msg.setWindowTitle("Error: Missing Values")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    # deals with issue regarding Type v Core Type and Interval v Interval (cm)
    def unifyHeaderNames(self, columns):
        # replace some variations on important names
        if("Core Type" in columns):
            columns[columns.index("Core Type")] = "Type"
        for header in columns:
            if("Interval" in header):
                columns[columns.index(header)] = "Interval"
                break
        return columns

    # determines if an uploaded file has the required Site, Hole, Core, Type, Section, and Interval data
    def isFileValid(self, key, filename):
        valid = True
        missingFields = []
        neededData = ["Site", "Hole", "Core", "Type", "Section", "Interval"]

        # get all headers from the uploaded file
        file = open(filename, 'r')
        reader = csv.DictReader(file)
        dict_from_csv = dict(list(reader)[0])
        columns = list(dict_from_csv.keys())

        # does it have all the data we need? what data is it missing?
        for i in neededData:
            if(not (i in columns)):
                missingFields.append(i)

        # Were they missing something?
        if(len(missingFields) > 0):
            valid = False

        if(not valid):
            self.createFileErrorMsgBox(missingFields, columns)
        else:
            return 1
        return 0

    # add retrieved data to the dictionary containing all XRF data
    def addToDictMaster(self, fname):
        # create the dictionary for this file
        app.dictMaster[fname] = {}
        # used to find these columns from XRF file and init the dictionary for this file
        neededData = ["Site", "Hole", "Core", "Section"]
        # see if Type is present in some capacity, if so add Type to needed Data because it is present in the file
        vals = self.isHeaderInFile("Type", fname)
        if(vals != "null"):
            neededData.append(vals)

        # see if interval is present in some capacity, if so add Type to needed Data because it is present in the file
        vals = self.isHeaderInFile("Interval", fname)
        if(vals != "null"):
            neededData.append("Interval")

        # create the dictionary with neededData columns from above
        file = pd.read_csv(fname, usecols=neededData)
        # create the file entry in dictMaster the key is the full path to uploaded file
        app.dictMaster[fname] = file.to_dict(orient='list')

        # loop through all known elements
        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, fname)
            if temp[0]:
                # append to a list of elements found in all uploaded XRF files
                global xrfElements
                xrfElements.append(element)
                # find the column with the current element
                df = pd.read_csv(fname, usecols=[temp[1]])
                # add a list of the current elements data from the uploaded file to the dictMaster[filename][element] : [data1,data2,data3 ...]
                app.dictMaster[fname].update(df.to_dict(orient='list'))
                app.dictMaster[fname][element] = app.dictMaster[fname].pop(
                    temp[0])
        # replace all non numeric data with zero
        self.removeNonNumericDictMasterData()

    # add retrieved data to the dictionary containing all Concentration data
    def addToConDict(self, fname):
        # create the dictionary for this file
        app.conDict[fname] = {}
        # used to find these columns from XRF file and init the dictionary for this file
        neededData = ["Site", "Hole", "Core", "Section"]

        # see if Type is present in some capacity, if so add Type to needed Data because it is present in the file
        vals = self.isHeaderInFile("Type", fname)
        if(vals != "null"):
            neededData.append(vals)
        # see if interval is present in some capacity, if so add Type to needed Data because it is present in the file
        vals = self.isHeaderInFile("Interval", fname)
        if(vals != "null"):
            neededData.append("Interval")

        # create the dictionary with neededData columns from above
        file = pd.read_csv(fname, usecols=neededData)
        app.conDict[fname] = file.to_dict(orient='list')
        count = 0

        # loop through all known elements
        for element in elements:
            # Figure out if element column is present in file. Temp consists of Object (or none) and column index (or -1)
            temp = self.isElementInFile(element, fname)
            if temp[0]:
                # update list with all elements found in this concentration file
                global elementsToDisplay
                elementsToDisplay.append(temp[0])
                # add to the concentration dictionary the data collected from this file for current element
                df = pd.read_csv(fname, usecols=[temp[1]])
                # add a list of the current elements data from the uploaded file to the conDict[filename][element] : [data1,data2,data3 ...]
                app.conDict[fname].update(df.to_dict(orient='list'))
                app.conDict[fname][element] = app.conDict[fname].pop(temp[0])
        # replace all non numeric data with zero
        self.removeNonNumericConDictData()

    # parse through every element in each file of conDict and replace all non numeric input with the int equivalent or zero
    def removeNonNumericConDictData(self):
        # all files in conDict
        for file in app.conDict:
            # all column headers in the file dictionary
            for key in app.conDict[file]:
                # if the header is an element
                if(key in elements):
                    # loop through the values
                    for i in range(0, len(app.conDict[file][key])):
                        # if the value is a string
                        if(isinstance(app.conDict[file][key][i], str)):
                            # see if the string can be parsed directly into an int
                            try:
                                app.conDict[file][key][i] = int(
                                    app.conDict[file][key][i])
                            # string is not a number so we make it zero
                            except ValueError:
                                app.conDict[file][key][i] = 0

    # parse through every element in each file of dictMaster and replace all non numeric input with the int equivalent or zero

    def removeNonNumericDictMasterData(self):
        # all files in conDict
        for file in app.dictMaster:
            # all column headers in the file dictionary
            for key in app.dictMaster[file]:
                # if the header is an element
                if(key in elements):
                    # loop through the values
                    for i in range(0, len(app.dictMaster[file][key])):
                        # if the value is a string
                        if(isinstance(app.dictMaster[file][key][i], str)):
                            #print("Found string: "+ app.dictMaster[file][key][i])
                            # see if the string can be parsed directly into an int
                            try:
                                app.dictMaster[file][key][i] = int(
                                    app.dictMaster[file][key][i])
                            # string is not a number so we make it zero
                            except ValueError:
                                app.dictMaster[file][key][i] = 0

    # given a header (key) and filename, this will determine if it exists in the file, null otherwise

    def isHeaderInFile(self, key, fileName):
        file = open(fileName, 'r')
        reader = csv.reader(file)
        headerRow = list(reader)[0]
        for header in headerRow:
            if(key in header):
                return header
        return "null"

    # given an element (Fe) and filename, will determine if a column header contains that element with some regex to handle different string literals
    def isElementInFile(self, element, fileName):
        file = open(fileName, 'r')
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

    # allow the wizard to advance if there is at least one XRF file uploaded and one concentration file is present
    def isComplete(self):
        return self.XRFInput.item(1) is not None and self.conInput.item(1) is not None
