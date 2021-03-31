import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint

class ElementSelectorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        layout = QGridLayout(self)
        label = QLabel("Choose Elements")
        layout.addWidget(label)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.MultiSelection)
        for i in range(1,21):
            self.listwidget.insertItem(i, str(i))

        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

        nextButton = QPushButton("Continue")
        nextButton.clicked.connect(self.confirmElementSelection)
        layout.addWidget(nextButton)
        self.setLayout(layout)

    def clicked(self, qmodelindex):
        items = self.listwidget.selectedItems()
        value = [i.text() for i in list(items)]
        print(value)

    def confirmElementSelection(self):
        print("Next Window")
        self.close()
