from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

class OptionsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(OptionsPage, self).__init__(parent)

        self.outputpath = ""
        self.majorAxis = False

        layout = QGridLayout(self)
        label = QLabel("Output and Regression")
        layout.addWidget(label)

        linearButt = QRadioButton("Standard Regression")
        linearButt.setChecked(True)
        linearButt.clicked.connect(self.linearSelected)
        layout.addWidget(linearButt)

        majorAx = QRadioButton("Major Axis Regression")
        majorAx.setChecked(False)
        majorAx.clicked.connect(self.majorSelected)
        layout.addWidget(majorAx)

        lab = QLabel("Output File Destination:")
        layout.addWidget(lab)

        self.pathLabel = QLabel(self.outputpath)
        layout.addWidget(self.pathLabel)

        text = "Browse"
        browseButt = QPushButton(text)
        browseButt.setMaximumWidth(100)
        browseButt.clicked.connect(self.browseFileLocation)
        layout.addWidget(browseButt)

        self.setLayout(layout)


    def browseFileLocation(self):
        fileName = QFileDialog.getSaveFileName(self, 'Output file location', '')
        self.outputpath = str(fileName[0])
        self.pathLabel.setText(self.outputpath)
        self.completeChanged.emit()

    def isComplete(self):
        return self.outputpath != ""

    def majorSelected(self):
        self.majorAxis = True

    def linearSelected(self):
        self.majorAxis = False
