from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from elements import *
from input import *

class ElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ElementSelectorPage, self).__init__(parent)
        layout = QGridLayout(self)
        label = QLabel("Choose Elements")
        layout.addWidget(label)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        for i in range(1,70):
            self.listwidget.insertItem(i, str(i))

        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

        self.setLayout(layout)

        self.selectedElements = []

    def clicked(self, qmodelindex):
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]
        #print(self.selectedElements)
