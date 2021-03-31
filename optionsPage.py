from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class OptionsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(OptionsPage, self).__init__(parent)
        layout = QGridLayout(self)
        label = QLabel("User Specifications")
        layout.addWidget(label)

        for i in range(0,10):
            checks = QCheckBox()
            checks.setText("Option " + str(i+1))
            layout.addWidget(checks)

        self.setLayout(layout)
