from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import inputSelectorPage

elementsToGraph = []

class ElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ElementSelectorPage, self).__init__(parent)
        layout = QGridLayout(self)
        label = QLabel("Choose Elements")
        layout.addWidget(label)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listwidget.clicked.connect(self.clicked)
        

        layout.addWidget(self.listwidget)

        self.setLayout(layout)

        self.selectedElements = []

    def clicked(self, qmodelindex):
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]

        global elementsToGraph
        elementsToGraph = self.selectedElements
        print(elementsToGraph)

    def initializePage(self):
        temp = sorted(set(inputSelectorPage.elementsToDisplay))
        num = 1
        print("-----BUG----\nThis list can have odd functionality")
        for element in temp:
            self.listwidget.insertItem(num, str(element))
            num = num + 1
