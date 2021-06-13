from PyQt5 import QtWidgets
import graphPage


class OptionsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(OptionsPage, self).__init__(parent)

        # basic setup layout and title
        layout = QtWidgets.QGridLayout(self)
        label = QtWidgets.QLabel("Output and Regression")
        layout.addWidget(label)
        self.outputpath = ""

        # Create radio button to select linear regression
        linearButt = QtWidgets.QRadioButton("Standard Linear Regression")
        linearButt.setChecked(True)
        linearButt.clicked.connect(self.linearSelected)
        layout.addWidget(linearButt)

        # create radio button to select major axis regression
        majorAx = QtWidgets.QRadioButton("Major Axis Regression")
        majorAx.setChecked(False)
        majorAx.clicked.connect(self.majorSelected)
        layout.addWidget(majorAx)

        # add label to select output destination and show selected destination
        lab = QtWidgets.QLabel("Output File Destination:")
        layout.addWidget(lab)
        self.pathLabel = QtWidgets.QLabel(self.outputpath)
        layout.addWidget(self.pathLabel)

        # Create browse button and spawn a file picker for the user to choose name and location for output file
        text = "Browse"
        browseButt = QtWidgets.QPushButton(text)
        browseButt.setMaximumWidth(100)
        browseButt.clicked.connect(self.browseFileLocation)
        layout.addWidget(browseButt)

        self.setLayout(layout)

    # allow the user to choose an output file location
    def browseFileLocation(self):
        # open a file browser
        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Output file location', '')
        # set output path to selected path and update label so user can see selected destination
        self.outputpath = str(fileName[0])
        self.pathLabel.setText(self.outputpath)
        # used to extract file name from file path on next page
        graphPage.fileName = self.outputpath
        # notify app of changes
        self.completeChanged.emit()

    # allow the user to advance if a save file location has been picked
    def isComplete(self):
        return self.outputpath != ""

    # sets flag for major axis regrssion
    def majorSelected(self):
        graphPage.majorAxisRegressionSelected = True

    # sets flag for standard linear regression
    def linearSelected(self):
        graphPage.majorAxisRegressionSelected = False
