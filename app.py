import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from elements import *
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        apply_stylesheet(app, theme='dark_teal.xml')
        self.setWindowTitle("MaXelerate")
        btn = QPushButton("Open File")
        elementsBtn = QPushButton("Show Elements")
        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(elementsBtn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        btn.clicked.connect(self.open) # connect clicked to self.open()
        elementsBtn.clicked.connect(self.show_new_window)
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
        
    def show_new_window(self, checked):
        self.w = ElementSelectorWindow()
        self.w.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()
