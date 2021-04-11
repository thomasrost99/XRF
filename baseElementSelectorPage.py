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
        #buttons = []

        #self.listwidget = QListWidget()
        #self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        #self.listwidget.clicked.connect(self.clicked)
        #layout.addWidget()


    def clicked(self, qmodelindex):
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]

        global elementsToGraph
        elementsToGraph = self.selectedElements
        print(elementsToGraph)

    def showSelected(self):
        for butt in buttons:
            if(butt.isChecked()):
                print(butt.text() + " is selected")
                break

    def updateLabel(self, value):
        rbtn = self.sender()
        if rbtn.isChecked() == True:
            global baseElement
            print(baseElement)
            baseElement = rbtn.text()
            print(baseElement)

    def initializePage(self):

        self.layout = QGridLayout(self)
        label = QLabel("Choose Base Elements")
        self.layout.addWidget(label)
        self.setLayout(self.layout)
        self.selectedElements = []

        temp = sorted(set(inputSelectorPage.elementsToDisplay))
        buttons.clear()

        for element in temp:
            #self.listwidget.insertItem(num, str(element))
            buttAdd = QRadioButton(str(element))
            buttAdd.setChecked(False)
            buttons.append(buttAdd)
            buttAdd.toggled.connect(self.updateLabel)

        for butt in buttons:
            self.layout.addWidget(butt)
