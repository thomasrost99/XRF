import sys
import random
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint

class InputSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(InputSelectorPage,self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Initialize window with format
        layout = QGridLayout(self)

        # Create first column header and add to layout
        labelOne = QLabel("Add XRF files...")
        labelOne.setAlignment(Qt.AlignHCenter)
        layout.addWidget(labelOne, 0, 0)

        # Create second column header and add to layout
        labelTwo = QLabel("Add a Concentration file...")
        labelTwo.setAlignment(Qt.AlignHCenter)
        layout.addWidget(labelTwo, 0, 1)

        # Create XRF list widget and add to the first column
        self.XRFInput = QListWidget()
        self.XRFInput.setSelectionMode(QAbstractItemView.SingleSelection)
        self.XRFInput.insertItem(0, "Add an XRF file...")
        self.XRFInput.clicked.connect(self.XRFClicked)
        layout.addWidget(self.XRFInput, 1, 0)

        # Create Calibration list widget and add to the second column
        self.calibrationInput = QListWidget()
        self.calibrationInput.setSelectionMode(QAbstractItemView.SingleSelection)
        self.calibrationInput.insertItem(0, "Add a Calibration file...")
        self.calibrationInput.clicked.connect(self.CalClicked)
        layout.addWidget(self.calibrationInput, 1, 1)

        layout.setVerticalSpacing(10)
        self.setLayout(layout)

    # If "add" item is clicked in XRF input, choose a new csv file to add to the list. If any other list item is clicked,
    # it should be removed.
    def XRFClicked(self, qmodelindex):
        if(self.XRFInput.currentItem().text() == "Add an XRF file..."):
            dialog = QFileDialog
            res = dialog.getOpenFileName(self, 'Open file', '',"Csv files (*.csv)")
            if(res[0]):
                self.XRFInput.insertItem(1, res[0])
                self.isFileVaid()
        else:
            self.XRFInput.takeItem(self.XRFInput.currentRow())
        self.XRFInput.clearSelection()

    # If the "add" item is clicked in Calibration input, choose a new csv file to add to the list. If the only item in the list
    # is selected again, choose a new file to replace it.
    def CalClicked(self, qmodelindex):
        dialog = QFileDialog
        res = dialog.getOpenFileName(self, 'Open file', '',"Csv files (*.csv)")
        # file = open(res[0] ,'r')
        # reader = csv.reader(file)
        # file.close()
        if(res[0]):
            self.calibrationInput.insertItem(1, res[0])
            items = self.calibrationInput.selectedItems()
            value = [i.text() for i in list(items)]
            self.calibrationInput.takeItem(0)
            self.isFileVaid()
        self.calibrationInput.clearSelection()


    def isFileVaid(self):
        print("check if file has info we need")
        missingFields = ["name","core","cooter"]
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Uploaded file is missing the following column headers: ")
        add = ""
        for i in range(0,len(missingFields)):
            add += missingFields[i] + ", "
        msg.setInformativeText(add)
        msg.setWindowTitle("Error: Missing Values")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def msgbtn(self, i):
        print("Button pressed: " + i.text())


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
