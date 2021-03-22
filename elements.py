import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
