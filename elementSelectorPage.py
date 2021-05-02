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

        #creates layout and titles for page
        layout = QGridLayout(self)
        label = QLabel("Choose Elements")
        layout.addWidget(label,1,1)

        #creates a list widget to hold elements
        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listwidget.itemSelectionChanged.connect(self.clicked)
        layout.addWidget(self.listwidget,2,1)
        self.setLayout(layout)
        self.selectedElements = []

    #each time the list is clicked update which elements have been selected in the list
    def clicked(self):
        #add all highlightd elements to the list of currently selected elements
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]

        #update the elements that should be graphed
        global elementsToGraph
        elementsToGraph = self.selectedElements

        #notify the app of changes
        self.completeChanged.emit()

    def initializePage(self):
        #selected base element
        baseEl = baseElementSelectorPage.baseElement

        #intersect the lists without the base element and sort alphabetically
        temp  = sorted(set(list(set(inputSelectorPage.xrfElements) & set(inputSelectorPage.elementsToDisplay))))
        num = 1
        #clear the list
        self.listwidget.clear()

        #add all the selectable elements to the page
        for element in temp:
            #do not display the base element
            if(element != baseEl):
                self.listwidget.insertItem(num, str(element))
                num = num + 1

    #allows the user to advance if at least one element is selected
    def isComplete(self):
        return len(self.listwidget.selectedItems()) > 0
