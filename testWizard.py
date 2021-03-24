#!/usr/bin/env python
from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from elementSelectorPage import *
from inputSelectorPage import *
from qt_material import apply_stylesheet

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
        super(QIComboBox, self).__init__(parent)


class MacWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MacWizard, self).__init__(parent)
        self.setWindowTitle("MaXelerate")

        #apply styles
        #apply_stylesheet(app, theme='dark_blue.xml')
        self.setWizardStyle(1)

        # Define screen size
        global screenHeight, screenWidth
        screenHeight = app.primaryScreen().size().height()
        screenWidth = app.primaryScreen().size().width()
        #set size of wizard
        self.setGeometry(screenWidth//4, screenHeight//4, screenWidth//2, screenHeight//2)

        #create pages to add to wizard
        self.inputPage = InputSelectorPage(self)
        self.elementPage = ElementSelectorPage(self)

        global inputPageID, elementPageID
        inputPageID = 0
        elementPageID = 1
        #Add pages in order to the wizard
        self.setPage(inputPageID, self.inputPage)
        self.setPage(elementPageID, self.elementPage)



        #link all buttons to proper functions
        self.button(QWizard.NextButton).clicked.connect(self.nextClicked)
        self.button(QWizard.FinishButton).clicked.connect(self.finishClicked)
        self.button(QWizard.CancelButton).clicked.connect(self.cancelClicked)
        self.button(QWizard.BackButton).clicked.connect(self.backClicked)

    def nextClicked(self):
        print(QWizard.currentPage(self))
        print(QWizard.currentId(self))
        #self.button(QWizard.BackButton).setEnabled(False)
        #print(self.elementPage.selectedElements)

    def finishClicked(self):
        print("Make Output / Check if this replaced the next button")

    def cancelClicked(self):
        print("Cancelled")

    def backClicked(self):
        print("DAK IS BACK")

class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = MacWizard()
    wizard.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()
    #print('\n'.join(repr(w) for w in app.allWidgets()))
