import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#from elements import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w = AnotherWindow()
        self.w.show()

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


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
