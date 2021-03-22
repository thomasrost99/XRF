import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from elements import *

def window():
   app = QApplication(sys.argv)
   widget = QWidget()

   layout = QVBoxLayout()
   textLabel = QLabel(widget)
   textLabel.setText("<h1>Jack is a retard whore!</h1>")
   #textLabel.move(10,10)
   layout.addWidget(textLabel)

   layout.addWidget(QPushButton("Upload File"))

   button2 = QPushButton("Choose Element")
   button2.clicked.connect(showElements)
   layout.addWidget(button2)

   layout.addWidget(QPushButton("Make Graph"))

   widget.setGeometry(300,300,300,300)
   widget.setWindowTitle("PyQt5 Example")
   widget.setLayout(layout)
   widget.show()

   sys.exit(app.exec_())

def showElements():
    print("Helloo")


if __name__ == '__main__':
    window()
