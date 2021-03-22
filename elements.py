import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

class Element(QWidget):

    def __init__(self):
        super(Element, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        #self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.show()
