import signal
import sys
import signal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from elements import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
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

    def show_new_window(self, checked):
        self.w = ElementSelectorWindow()
        self.w.show()

    def open(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*.*)')
        if path != ('', ''): print("File path : "+ path[0])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()
