from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import inputSelectorPage

baseElement = ""
buttons = []

class BaseElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(BaseElementSelectorPage, self).__init__(parent)


    def updateLabel(self, value):
        rbtn = self.sender()
        if rbtn.isChecked() == True:
            global baseElement
            baseElement = rbtn.text()
        self.completeChanged.emit()

    def initializePage(self):

        self.layout = QGridLayout(self)
        label = QLabel("Choose Base Element")
        self.layout.addWidget(label)
        self.setLayout(self.layout)
        self.selectedElements = []

        temp = sorted(set(inputSelectorPage.elementsToDisplay))
        buttons.clear()

        for element in temp:
            #self.listwidget.insertItem(num, str(element))
            buttAdd = QRadioButton(str(element))
            global baseElement
            if element == baseElement:
                buttAdd.setChecked(True)
            else:
                buttAdd.setChecked(False)
            buttons.append(buttAdd)
            buttAdd.toggled.connect(self.updateLabel)

        for butt in buttons:
            self.layout.addWidget(butt)

    def isComplete(self):
        flag = False
        for butt in buttons:
            if(butt.isChecked()):
                flag = True
                break
        return flag