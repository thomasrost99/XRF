from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import inputSelectorPage
import baseElementSelectorPage

elementsToGraph = []

class ElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ElementSelectorPage, self).__init__(parent)
        layout = QGridLayout(self)
        label = QLabel("Choose Elements")
        layout.addWidget(label,1,1)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listwidget.itemSelectionChanged.connect(self.clicked)

        layout.addWidget(self.listwidget,2,1)

        self.setLayout(layout)

        self.selectedElements = []



    def clicked(self):
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]

        global elementsToGraph
        elementsToGraph = self.selectedElements
        print(elementsToGraph)
        self.completeChanged.emit()

    def initializePage(self):
        #print(set(inputSelectorPage.xrfElements))
        #print(set(inputSelectorPage.elementsToDisplay))
        baseEl = baseElementSelectorPage.baseElement
        print(baseEl)
        if(baseEl in inputSelectorPage.xrfElements):
            inputSelectorPage.xrfElements.remove(baseEl)
        if(baseEl in inputSelectorPage.elementsToDisplay):
            inputSelectorPage.elementsToDisplay.remove(baseEl)

        temp  = sorted(set(list(set(inputSelectorPage.xrfElements) & set(inputSelectorPage.elementsToDisplay))))
        #print(temp)
        #temp = sorted(set(temp))
        num = 1
        self.listwidget.clear()
        for element in temp:
            self.listwidget.insertItem(num, str(element))
            num = num + 1

    def isComplete(self):
        return len(self.listwidget.selectedItems()) > 0
