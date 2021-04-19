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
import app
import os
from os import listdir
from os.path import isfile, join
import elementSelectorPage
import baseElementSelectorPage
from pylr2 import regress2

fileName = ""
majorAxisRegressionSelected = False

class GraphPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(GraphPage, self).__init__(parent)
        self.layout = QGridLayout(self)
        label = QLabel("Select a graph to view")
        self.layout.addWidget(label)

        self.dropDown = QComboBox(self)
        self.dropDown.activated[str].connect(self.onChanged)
        self.layout.addWidget(self.dropDown)

        fileName = ""

        self.pic = QPixmap("")
        self.picLabel = QLabel()
        self.picLabel.setPixmap(self.pic)
        self.layout.addWidget(self.picLabel)

        self.setLayout(self.layout)

        self.onlyfiles = []
        self.elements = []

        if not os.path.exists('./GraphImages/'):
            os.makedirs('./GraphImages/')


        #-----------------------------------------------------------------------------------------


    def initializePage(self):
        global fileName
        if "." in fileName:
            fileName = fileName[:fileName.find(".")]
        #if ".pdf" not in fileName:
            #fileName = fileName + ".pdf"

        print(fileName)
        filelist = [ f for f in os.listdir("./GraphImages/") if f.endswith(".png") ]
        for f in filelist:
            os.remove(os.path.join("./GraphImages/", f))

        # This list contains the elements that were selected on elementSelectorPage
        self.elements = elementSelectorPage.elementsToGraph
        print("Making Graphs")
        temp = fileName + ".pdf"
        pdf = matplotlib.backends.backend_pdf.PdfPages(temp)

        ### DATAFRAMES MERGER

        try:
            energy_levels = []

            for key, value in app.dictMaster.items():
                energy_level = key[-8:-4]
                if(not energy_level in energy_levels):
                    energy_levels.append(energy_level)

            xrf_data = pd.DataFrame()

            for el in energy_levels:
                el_temp_df = pd.DataFrame()
                for key, value in app.dictMaster.items():
                    if el in key:
                        temp_df = pd.DataFrame.from_dict(value)
                        el_temp_df = el_temp_df.append(temp_df)
                if(energy_levels.index(el) == 0):
                    xrf_data = el_temp_df
                else:
                    xrf_data = pd.merge(xrf_data, el_temp_df,how='outer', on=['Site', 'Hole' ,'Core', 'Type', 'Section', "Interval"])

            conc_data = pd.DataFrame()

            for key, value in app.conDict.items():
                temp_df = pd.DataFrame.from_dict(value)
                conc_data = conc_data.append(temp_df)

            base_elem = baseElementSelectorPage.baseElement
            xrf_data = xrf_data[(xrf_data != 0).all(1)]
            conc_data = conc_data[(conc_data != 0).all(1)]
            output_data = xrf_data

            dict_for_plots = {}

            for element in self.elements:
                ## Calculating Log Ratios for both files
                ### DO NOT INCLUDE NEGATIVE VALUES
                conc_data[element+'/'+base_elem] = np.log(conc_data[element]/conc_data[base_elem])
                xrf_data['ln('+element+'/'+base_elem+')'] = np.log(xrf_data[element]/xrf_data[base_elem])

                ## Finding Equivalent data
                elem_base_master = pd.DataFrame(columns = ['Conc', 'Scanner'])
                for i in conc_data.index:
                    hole_scanner = xrf_data[xrf_data['Hole'] == conc_data['Hole'][i]]
                    core_scanner = hole_scanner[hole_scanner['Core'] == conc_data['Core'][i]]
                    section_scanner = core_scanner[core_scanner['Section'] == conc_data['Section'][i]]
                    interval_scanner = section_scanner[section_scanner['Interval'] == conc_data['Interval'][i]]
                    if interval_scanner.shape[0] == 0:
                        interval_scanner = section_scanner[section_scanner['Interval'] == conc_data['Interval'][i]+1]
                        if interval_scanner.shape[0] == 0:
                            interval_scanner = section_scanner[section_scanner['Interval'] == conc_data['Interval'][i]+2]
                            if interval_scanner.shape[0] == 0:
                                continue
                    elem_base_master = elem_base_master.append({'Conc': conc_data[element+'/'+base_elem][i], 'Scanner': np.mean(interval_scanner['ln('+element+'/'+base_elem+')'])},
                                    ignore_index = True)
                elem_base_master.columns = ['ln('+element+'/'+base_elem+')_Conc', 'ln('+element+'/'+base_elem+')_XRF']

                ## Building Regression Model
                elem_base_master_final = elem_base_master.dropna()
                if elem_base_master_final.shape[0] == 0:
                    continue
                X = np.array(elem_base_master_final['ln('+element+'/'+base_elem+')_XRF']).reshape(-1, 1)
                Y = np.array(elem_base_master_final['ln('+element+'/'+base_elem+')_Conc']).reshape(-1, 1)
                
                if(majorAxisRegressionSelected):
                    results = regress2(X, Y, _method_type_2="reduced major axis")
                    slope = 0
                    intercept = 0
                    r_score = 0
                    for key, value in results.items():
                        if key == "slope":
                            slope = value
                        elif key == "intercept":
                            intercept = value
                        elif key == "r":
                            r_score = value
                    dict_for_plots[element+'/'+base_elem] = {'x_val': X, 'y_val': Y, 'r_score': r_score,
                        'coef': slope, 'intercept': intercept}
                    log_predicted = np.array(xrf_data['ln('+element+'/'+base_elem+')']).reshape(-1, 1)*slope + intercept
                    
                else:
                    regr = LinearRegression()
                    regr.fit(X, Y)
                    score = regr.score(X,Y)
                    dict_for_plots[element+'/'+base_elem] = {'x_val': X, 'y_val': Y, 'r_score': score,
                        'coef': regr.coef_[0][0], 'intercept': regr.intercept_[0]}

                    log_predicted = np.array(xrf_data['ln('+element+'/'+base_elem+')']).reshape(-1, 1)*regr.coef_[0][0] + regr.intercept_[0]

                
                predicted_ratio = np.exp(log_predicted)
                output_data['predicted_ln('+element+'/'+base_elem+')'] = log_predicted
                output_data['predicted_'+element+'/'+base_elem] = predicted_ratio

            output_data.to_csv(fileName + ".csv", index=False)
        except:
            print("Error Occured!")

        for plot in dict_for_plots:
            fig = plt.figure()
            plt.scatter(dict_for_plots[plot]["x_val"], dict_for_plots[plot]["y_val"], color ='b')
            plt.plot(dict_for_plots[plot]["x_val"], dict_for_plots[plot]["coef"] * dict_for_plots[plot]["x_val"] + dict_for_plots[plot]["intercept"], color ='k')
            plt.xlabel("Log Ratio of XRF Scanner")
            plt.ylabel("Log Ratio of Concentration")
            plt.title(str(plot))
            r = round(dict_for_plots[plot]["r_score"], 5)
            plt.text(0.1,0.9,"r^2 = {}".format(r),transform=plt.gca().transAxes)
            eq = "y = " + str(round(dict_for_plots[plot]["coef"], 2)) + "x + " + str(round(dict_for_plots[plot]["intercept"], 2))
            plt.text(0.1,0.85, eq, transform=plt.gca().transAxes)
            #plt.show()
            plt.savefig('GraphImages/'+ plot.replace("/", "") + '.png')
            pdf.savefig(fig)

        pdf.close()

        onlyfiles = [f for f in listdir("./GraphImages/") if isfile(join("./GraphImages/", f))]

        self.dropDown.clear()
        for file in onlyfiles:
            self.dropDown.addItem(file)



    def onChanged(self, text):
        self.layout.removeWidget(self.picLabel)
        self.pic = QPixmap("./GraphImages/" + str(text))
        self.picLabel = QLabel()
        self.picLabel.setPixmap(self.pic)
        self.layout.addWidget(self.picLabel)
