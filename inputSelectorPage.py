import sys
import random
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint
#import openpyxl
import pandas as pd
import csv


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
        nextButton = QPushButton("Test File Parsing")
        nextButton.clicked.connect(self.testInputParse)
        layout.addWidget(nextButton, 3, 0, 1, 2)

        layout.setVerticalSpacing(10)
        self.setLayout(layout)

    # If "add" item is clicked in XRF input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def XRFClicked(self, qmodelindex):
        if(self.XRFInput.currentItem().text() == "Add an XRF file"):
            dialog = QFileDialog
            res = dialog.getOpenFileName(self, 'Open file', '',"Csv files (*.csv)")
            if(res[0]):
                duplicate = 0
                for i in range(self.XRFInput.count()):
                    if(res[0] == self.XRFInput.item(i).text()):
                        duplicate = 1
                if not duplicate:
                    self.XRFInput.insertItem(1, res[0])
                    self.isFileVaid("XRF")
        else:
            self.XRFInput.takeItem(self.XRFInput.currentRow())
        self.XRFInput.clearSelection()

    # If "add" item is clicked in Concentration input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def ConClicked(self, qmodelindex):
        if(self.conInput.currentItem().text() == "Add a Concentration file"):
            dialog = QFileDialog
            res = dialog.getOpenFileName(self, 'Open file', '',"Csv files (*.csv)")
            if(res[0]):
                duplicate = 0
                for i in range(self.conInput.count()):
                    if(res[0] == self.conInput.item(i).text()):
                        duplicate = 1
                if not duplicate:
                    self.conInput.insertItem(1, res[0])
                    self.isFileVaid("Concentration")
        else:
            self.conInput.takeItem(self.conInput.currentRow())
        self.conInput.clearSelection()

    def createFileErrorMsgBox(self, missingFields):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Update the file to include the headers listed below:")
        msg.setInformativeText('\n'.join(missingFields))
        #detailed = "Missing Headers:\n" + '\n'.join(missingFields)
        #msg.setDetailedText(detailed)
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

    def isFileVaid(self, key):
        valid = True
        print("check if file has info we need")
        missingFields = []
        neededData = ["Site","Hole","Core", "Type","Section","Interval"]

        #concentration file validation
        if(key=="Concentration"):
            filename = self.conInput.item(1).text()
        #XRF file validation
        elif(key=="XRF"):
            filename = self.XRFInput.item(1).text()
        else:
            valid = False

        print("File: ", filename)
        file = open(filename , 'r')
        reader = csv.DictReader(file)
        dict_from_csv = dict(list(reader)[0])
        columns = list(dict_from_csv.keys())
        columns = self.unifyHeaderNames(columns)
        print("Columns ", columns)

        # columns = parse itrax, parse avaa
        #concentrations and U files already are good

        #does it have all the data we need? what data is it missing?
        for i in neededData:
            if(not (i in columns)):
                missingFields.append(i)

        #-----------TODO--------add check for valid element

        #Were they missing something?
        if(len(missingFields)>0):
            valid = False

        if(not valid):
            if(key=="XRF"):
                self.XRFInput.takeItem(1)
            elif(key=="Concentration"):
                self.conInput.takeItem(1)
            self.createFileErrorMsgBox(missingFields)
            #remove file from list
        return


    def msgbtn(self, i):
        if(i.text()=="Retry"):
            print("Enter Info")

        print("Button pressed: " + i.text())

    # Close input window. Eventually will need to pass all file data to next "module"
    def testInputParse(self):
        print("Testing Input Parsing")
        print(self.XRFInput.item(1).text())
        file = open(self.XRFInput.item(1).text() ,'r')
        reader = csv.reader(file)
        line_count = 0
        # print(reader.__next__())
        reader.__next__()
        spectrum = reader.__next__()[0]
        print("Not parsed", spectrum)
        testOut = spectrum.replace('-', ' ').split(' ')
        print(testOut)
        sectionCoreType = testOut[2]
        section, coreType = list(testOut[2])
        print(testOut)
        print(section)
        print(coreType)
        testOut[2] = section
        testOut.insert(3,coreType)
        print(testOut)

        # Split up index 2


        # for row in reader:
        #     print(row[5])
        #     line_count += 1
        file.close()

    # Data we need from csv files:
    # For primary key:
    # Spectrum column will need to be broken down into
    # 374-U1524A-1H-1-A_SHLF9353571 X  20.0mm
    # Expedition: 374
    # SiteID: U1524A
    # Hole: 1
    # Core Type: H
    # Section: 1
    # Offset: X 20.0mm OR X1120.00mm
    # For calibration:
    # Hole, Core Type, Section, Offset (mm),
