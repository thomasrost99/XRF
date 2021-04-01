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
        nextButton.clicked.connect(self.makeInputFileIdeal)
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
        else:
            self.conInput.takeItem(self.conInput.currentRow())
        self.conInput.clearSelection()

    # goes through list of elements, so will not check for multiple headers with same beginning element in name
    def makeInputFileIdeal(self, filename):
        idealInput = []
        idealInput.append([])
        with open("Input_Files/XRF/Avaatech_BAxil_v1_30kV.xlsx - Avaatech_BAxil_v1_30kV_raw (1) - temp.csv", 'w') as f:
            writer = csv.writer(f)
            for element in elements:
                temp = self.isElementInFile(element,"Input_Files/XRF/Avaatech_BAxil_v1_30kV.xlsx - Avaatech_BAxil_v1_30kV_raw (1).csv")
                if temp[0]:
                    idealInput[0].append(temp[0])
                    df = pd.read_csv("Input_Files/XRF/Avaatech_BAxil_v1_30kV.xlsx - Avaatech_BAxil_v1_30kV_raw (1).csv", usecols = [temp[1]])
                    # print(df)

            
            print(len(idealInput[0]))
            print(idealInput)
            # writer.writerow(idealInpp)
            # writer.writerow(['test 1'])
            # writer.writerow(["test 2"])
            # f.seek(0)
            # writer.writerow(["test 3"])

    
    def isElementInFile(self, element, fileName):
        file = open(fileName ,'r')
        reader = csv.reader(file)
        headerRow = next(reader)
        for index, header in enumerate(headerRow):
            if "std" not in header.lower():
                if re.search(element+'([0-9]|-|_|\s).*', header.strip()):
                    file.close()
                    return element, index
        file.close()
        return None, -1

    # Example file browser
    # dialog = QFileDialog
    # res = dialog.getOpenFileName(self, 'Open file', 'c:\\Users\\thoma\\Downloads',"Csv files (*.csv)")
    # file = open(res[0] ,'r')
    # reader = csv.reader(file)
    # line_count = 0
    # for row in reader:
    #    print(row[5])
    #    line_count += 1
    # file.close()
    # print(res[0])

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