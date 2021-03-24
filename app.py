import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from elements import *
from input import *
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Define screen size
        global screenHeight, screenWidth
        screenHeight = app.primaryScreen().size().height()
        screenWidth = app.primaryScreen().size().width()

        self.initUI()

    def initUI(self):
        # Initialize window with style and format
        apply_stylesheet(app, theme='dark_teal.xml')
        self.setWindowTitle("MaXelerate")
        self.layout = QGridLayout()
        self.layout.setVerticalSpacing(30)
        self.layout.setSpacing(50)
        self.layout.setContentsMargins(30,0,30,0)
        self.widget = QWidget()

        toolbutt = QToolButton()
        toolbutt.setArrowType(Qt.LeftArrow)
        toolbutt.show()
        #self.layout.addWidget(toolbutt,3,0)
        self.widget.setLayout(self.layout)
        #toolbutt.setGeometry(50, 50, 50, 50)
        self.setCentralWidget(self.widget)
        self.setGeometry(screenWidth//2 - screenWidth//4, screenHeight//3 - screenHeight//4, screenWidth//4, screenHeight//4)

        #fileText = QTextItem("<h1>MaXelerate<\h1>")

        # Create buttons
        openFileButton = QPushButton("Open File")
        elementsBtn = QPushButton("Show Elements")

        # Add buttons to layout
        #layout.addWidget(fileText, 0, 0)
        self.layout.addWidget(openFileButton, 1, 0)
        self.layout.addWidget(elementsBtn, 2, 0)

        # Call button functions on click
        openFileButton.clicked.connect(self.open_input_window)
        elementsBtn.clicked.connect(self.open_element_window)

        self.show()

    # File browser functionality. Moved to input.py for the moment, may remove later.
    # def open(self):
    #     dialog = QFileDialog
    #     res = dialog.getOpenFileName(self, 'Open file', 'c:\\Users\\thoma\\Downloads',"Csv files (*.csv)")
    #     file = open(res[0] ,'r')
    #     reader = csv.reader(file)
    #     line_count = 0
    #     for row in reader:
    #        print(row[5])
    #        line_count += 1
    #     file.close()
    #     print(res[0])

    # Opens the element selector window
    def open_element_window(self, checked):
        wid = ElementSelectorWindow()
        #self.w.setGeometry(screenWidth//2 - screenWidth//4, screenHeight//2 - screenHeight//5, screenWidth//2, screenHeight//2)
        #self.w.show()
        self.layout.addWidget(wid)
        self.layout.itemAt(0).widget().hide()
        self.layout.itemAt(1).widget().hide()

        # Example to add a new button
        #tempButton = QPushButton("Temp")
        #self.centralWidget().layout().addWidget(tempButton, 3, 0)

    # Opens the file selector window
    def open_input_window(self, checked):
        self.w = InputSelectorWindow()
        self.w.setGeometry(screenWidth//2 - screenWidth//4, screenHeight//2 - screenHeight//5, screenWidth//2, screenHeight//3)
        self.w.show()

        # Example to delete the button added above
        if(self.centralWidget().layout().rowCount() > 3):
            self.centralWidget().layout().itemAtPosition(3,0).widget().close()

if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    window = MainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec_()
    # Will print all open objects
    print('\n'.join(repr(w) for w in app.allWidgets()))
