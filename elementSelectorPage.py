from PyQt5 import QtWidgets

import inputSelectorPage
import baseElementSelectorPage


class ElementSelectorPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ElementSelectorPage, self).__init__(parent)

        # creates layout and titles for page
        layout = QtWidgets.QGridLayout(self)
        label = QtWidgets.QLabel("Choose Elements")
        layout.addWidget(label, 1, 1)

        # creates a list widget to hold elements
        self.listwidget = QtWidgets.QListWidget()
        self.listwidget.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)
        self.listwidget.itemSelectionChanged.connect(self.clicked)
        layout.addWidget(self.listwidget, 2, 1)
        self.setLayout(layout)
        self.selectedElements = []

    # each time the list is clicked update which elements have been selected in the list
    def clicked(self):
        # add all highlightd elements to the list of currently selected elements
        items = self.listwidget.selectedItems()
        self.selectedElements = [i.text() for i in list(items)]

        # update the elements that should be graphed
        global elementsToGraph
        elementsToGraph = self.selectedElements

        # notify the app of changes
        self.completeChanged.emit()

    def initializePage(self):
        # intersect the lists without the base element and sort alphabetically
        temp = sorted(set(list(set(inputSelectorPage.xrfElements)
                      & set(inputSelectorPage.elementsToDisplay))))
        # clear the list
        self.listwidget.clear()

        # add all the selectable elements to the page
        for element in temp:
            # do not display the base element
            if(element != baseElementSelectorPage.baseElement):
                self.listwidget.addItem(str(element))

    # allows the user to advance if at least one element is selected
    def isComplete(self):
        return len(self.listwidget.selectedItems()) > 0
