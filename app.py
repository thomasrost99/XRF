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
from optionsPage import *
from graphPage import *
from qt_material import apply_stylesheet
from baseElementSelectorPage import *

dictMaster = {}
conDict = {}

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

        #maybe dont need
        self.setOption(QWizard.IndependentPages, False)

        # Define screen size
        global screenHeight, screenWidth
        screenHeight = app.primaryScreen().size().height()
        screenWidth = app.primaryScreen().size().width()
        #set size of wizard
        self.setGeometry(screenWidth//4, screenHeight//4, screenWidth//2, screenHeight//2)

        #create pages to add to wizard
        self.inputPage = InputSelectorPage(self)
        self.elementPage = ElementSelectorPage(self)
        self.optionsPage = OptionsPage(self)
        self.graphPage = GraphPage(self)
        self.baseElementPage = BaseElementSelectorPage(self)

        global inputPageID, elementPageID
        inputPageID = 0
        basePageID = 1
        elementPageID = 2
        optionsID = 3
        graphPageID = 4

        #Add pages in order to the wizard
        self.setPage(inputPageID, self.inputPage)
        self.setPage(basePageID, self.baseElementPage)
        self.setPage(elementPageID, self.elementPage)
        self.setPage(optionsID, self.optionsPage)
        self.setPage(graphPageID, self.graphPage)


        #link all buttons to proper functions
        self.button(QWizard.NextButton).clicked.connect(self.nextClicked)
        self.button(QWizard.FinishButton).clicked.connect(self.finishClicked)
        self.button(QWizard.CancelButton).clicked.connect(self.cancelClicked)
        self.button(QWizard.BackButton).clicked.connect(self.backClicked)

    def lockButton(self, name):
        print('LOCKED: ' + name)
        if(name=='back'):
            self.button(QWizard.BackButton).setEnabled(False)
        elif(name=='next'):
            self.button(QWizard.NextButton).setEnabled(False)
        elif(name=='cancel'):
            self.button(QWizard.CancelButton).setEnabled(False)
        elif(name=='finish'):
            self.button(QWizard.FinishButton).setEnabled(False)
        else:
            return False
        return True

    def unlockButton(self, name):
        print('UNLOCKED: ' + name)
        if(name=='back'):
            self.button(QWizard.BackButton).setEnabled(True)
        elif(name=='next'):
            self.button(QWizard.NextButton).setEnabled(True)
        elif(name=='cancel'):
            self.button(QWizard.CancelButton).setEnabled(True)
        elif(name=='finish'):
            self.button(QWizard.FinishButton).setEnabled(True)
        else:
            return False
        return True

    def nextClicked(self):
        pageID = QWizard.currentId(self)



    def finishClicked(self):
        print("finishClicked")

    def cancelClicked(self):
        print("Cancelled")

    def backClicked(self):
        print("back")



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = MacWizard()
    wizard.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()
    #print('\n'.join(repr(w) for w in app.allWidgets()))
