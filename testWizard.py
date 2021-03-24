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
        #apply_stylesheet(app, theme='dark_blue.xml')

        # Define screen size
        global screenHeight, screenWidth
        screenHeight = app.primaryScreen().size().height()
        screenWidth = app.primaryScreen().size().width()

        self.setWindowTitle("MaXelerate")
        self.addPage(ElementSelectorPage(self))
        self.addPage(InputSelectorPage(self))
        self.resize(screenWidth//4, screenHeight//4)

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
    print('\n'.join(repr(w) for w in app.allWidgets()))
