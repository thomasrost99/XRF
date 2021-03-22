import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

QWidget
{
    color: #b1b1b1;
    background-color: #323232;
    selection-background-color:#323232;
    selection-color: black;
    background-clip: border;
    border-image: none;
    border: 0px transparent black;
    outline: 0;
}

class MainWindow(QMainWindow):
   def __init__(self, parent=None):
      super(MainWindow, self).__init__(parent)
      self.setWindowTitle("MaXelerate")

      btn = QPushButton("Open File")
      layout = QHBoxLayout()
      layout.addWidget(btn)
      widget = QWidget()
      widget.setLayout(layout)
      self.setCentralWidget(widget)

      btn.clicked.connect(self.open) # connect clicked to self.open()
      self.setStyleSheet("border: 2px solid black; background:grey")
      self.show()

   def open(self):
      dialog = QFileDialog
      res = dialog.getOpenFileName(self, 'Open file', 'c:\\Users\\thoma\\Downloads',"Csv files (*.csv)")
      file = open(res[0] ,'r')
      reader = csv.reader(file)
      line_count = 0
      for row in reader:
         qDebug(row[5])
         line_count += 1
      file.close()
      qDebug(res[0])


if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   signal.signal(signal.SIGINT, signal.SIG_DFL)
   app.exec()