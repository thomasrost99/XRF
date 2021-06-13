from PyQt5 import QtWidgets

import inputSelectorPage

# global variables used to keep track of base element and radio buttons present on this page
baseElement = ""
buttons = []


class BaseElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(BaseElementSelectorPage, self).__init__(parent)

    # attached to each radio button, will change the base element when it is clicked
    def updateLabel(self, value):
        # get button attached to this function
        rbtn = self.sender()
        # if this element is selected
        if rbtn.isChecked():
            # change the currently selected base element
            global baseElement
            baseElement = rbtn.text()
        # notify the app that a new base element was selected
        self.completeChanged.emit()

    def initializePage(self):
        # setup laout and titles for the page
        self.layout = QtWidgets.QGridLayout(self)
        label = QtWidgets.QLabel("Choose Base Element")
        self.layout.addWidget(label)
        self.setLayout(self.layout)
        self.selectedElements = []

        # creates a list of elements that are present in XRF AND concentration files uploaded and sorts it in alphabetical order
        temp = sorted(set(list(set(inputSelectorPage.xrfElements)
                      & set(inputSelectorPage.elementsToDisplay))))
        buttons.clear()

        # for each element present in the intersection of XRF and concentraion files
        for element in temp:
            # create a button with the element name
            buttAdd = QtWidgets.QRadioButton(str(element))
            # if the current button is the selected base element, check it by default upon navigating back to this page
            global baseElement
            if element == baseElement:
                buttAdd.setChecked(True)
            else:
                buttAdd.setChecked(False)
            # add buttons to the list of all buttons in this page
            buttons.append(buttAdd)
            buttAdd.toggled.connect(self.updateLabel)

        # add all buttons to the page
        for butt in buttons:
            self.layout.addWidget(butt)

    # allows the user to advance if there is a selected button
    def isComplete(self):
        flag = False
        for butt in buttons:
            if(butt.isChecked()):
                flag = True
                break
        return flag
