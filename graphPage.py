from PyQt5 import QtCore, QtWidgets
import signal
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from PyQt5 import *
from random import randint
from qt_material import apply_stylesheet
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.backends.backend_pdf
from app import *
from os import listdir
from os.path import isfile, join
import elementSelectorPage



class GraphPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(GraphPage, self).__init__(parent)
        self.layout = QGridLayout(self)
        label = QLabel("Select a graph to view")
        self.layout.addWidget(label)

        self.dropDown = QComboBox(self)
        self.dropDown.activated[str].connect(self.onChanged)
        self.layout.addWidget(self.dropDown)


        self.pic = QPixmap("./GraphImages/test.png")
        self.picLabel = QLabel()
        self.picLabel.setPixmap(self.pic)
        self.layout.addWidget(self.picLabel)

        self.setLayout(self.layout)

        self.onlyfiles = []
        self.elements = []


        #-----------------------------------------------------------------------------------------


    def initializePage(self):
        # This list contains the elements that were selected on elementSelectorPage
        self.elements = elementSelectorPage.elementsToGraph
        print(self.elements)
        print("Making Graphs")
        pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")

        ## Reading Files
        conc = pd.ExcelFile("Input_Files/Concentration/U1456_concentrations.xlsx").parse()
        scanner_a = pd.ExcelFile("Input_Files/XRF/U1456A_10kV.xlsx").parse()
        scanner_c = pd.ExcelFile("Input_Files/XRF/U1456C_10kV.xlsx").parse()

        ## Calculating Log Ratios for both files
        conc['K/Ca'] = np.log(conc['K']/conc['Ca'])
        scanner_a['K/Ca'] = np.log(np.absolute(scanner_a['K_Area']/scanner_a['Ca_Area']))
        scanner_c['K/Ca'] = np.log(np.absolute(scanner_c['K_Area']/scanner_c['Ca_Area']))

        ## Finding Equivalent data
        K_Ca_master = pd.DataFrame(columns = ['Conc', 'Scanner'])
        for i in conc.index:
            if conc['Hole'][i] == "A":
                core_scanner = scanner_a[scanner_a['Core'] == conc['Core'][i]]
                section_scanner = core_scanner[core_scanner['Section'] == conc['Section'][i]]
                interval_scanner = section_scanner[section_scanner['Interval (cm)'] == conc['Interval (cm)'][i]]
                ### USING A RANGE FOR INTERVAL - WHAT IS THE OPTIMUM RANGE
                if interval_scanner.shape[0] == 0:
                    interval_scanner = section_scanner[section_scanner['Interval (cm)']
                                                   .between(conc['Interval (cm)'][i] - 2, conc['Interval (cm)'][i] + 2)]
                K_Ca_master = K_Ca_master.append({'Conc': conc['K/Ca'][i], 'Scanner': np.mean(interval_scanner['K/Ca'])},
                                  ignore_index = True)

            else:
                core_scanner = scanner_a[scanner_a['Core'] == conc['Core'][i]]
                section_scanner = core_scanner[core_scanner['Section'] == conc['Section'][i]]
                interval_scanner = section_scanner[section_scanner['Interval (cm)'] == conc['Interval (cm)'][i]]
                if interval_scanner.shape[0] == 0:
                    interval_scanner = section_scanner[section_scanner['Interval (cm)']
                                                   .between(conc['Interval (cm)'][i] - 2, conc['Interval (cm)'][i] + 2)]
                K_Ca_master = K_Ca_master.append({'Conc': conc['K/Ca'][i], 'Scanner': np.mean(interval_scanner['K/Ca'])},
                                  ignore_index = True)
        K_Ca_master.columns = ['ln(K/Ca)_Conc', 'ln(K/Ca)_XRF']

        ## Building Regression Model
        K_Ca_master_final = K_Ca_master.dropna()
        #### WHAT TO DO FOR NA VALUES
        X = np.array(K_Ca_master_final['ln(K/Ca)_XRF']).reshape(-1, 1)
        Y = np.array(K_Ca_master_final['ln(K/Ca)_Conc']).reshape(-1, 1)
        regr = LinearRegression()
        regr.fit(X, Y)

        ## Printing the R^2 value and the crossplot
        print(regr.score(X, Y))
        fig = plt.figure()
        plt.scatter(X, Y, color ='b')
        plt.xlabel("Log Ratio of XRF Scanner")
        plt.ylabel("Log Ratio of Concentration")
        plt.plot(X, regr.coef_[0][0] * X + regr.intercept_[0], color ='k')
        #plt.show()
        plt.savefig('GraphImages/test.png')
        pdf.savefig(fig)
        pdf.close()

        self.close()

        onlyfiles = [f for f in listdir("./GraphImages/") if isfile(join("./GraphImages/", f))]
        print(onlyfiles)

        for file in onlyfiles:
            self.dropDown.addItem(file)



    def onChanged(self, text):
        print(text)
        self.layout.removeWidget(self.picLabel)
        self.pic = QPixmap("./GraphImages/" + str(text))
        self.picLabel = QLabel()
        self.picLabel.setPixmap(self.pic)
        self.layout.addWidget(self.picLabel)
