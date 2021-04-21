import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

#DataSet1
ds1A = pd.read_csv("/AnswerKeys/DataSet1/U1456A_XRF_calibrations.csv")
ds1C = pd.read_csv("/AnswerKeys/DataSet1/U1456C_XRF_calibrations.csv")
ds1Us = pd.read_csv("/AnswerKeys/DataSet1/U1456_our_calculation_standard_regression.csv")

#DataSet2
ds2A =  pd.read_csv("/AnswerKeys/DataSet2/U1523A_dataset_answer_key.csv")
ds2B =  pd.read_csv("/AnswerKeys/DataSet2/U1523B_dataset_answer_key.csv")
ds2E =  pd.read_csv("/AnswerKeys/DataSet2/U1523E_dataset_answer_key.csv")
ds2Us =  pd.read_csv("/AnswerKeys/DataSet2/U1523_our_calculation_standard_regression.csv")

headers = ["Site", "Hole", "Core", "Type", "Section", "Interval"]
baseElementDS1 = "Ca"
elementsInDS1 = ["Al", "Si","P","S","Cl","Ar","K", "Ca", "Ti","Cr","Mn","Fe","Rh", "Ni","Cu", "Zn","Ga","Br","Rb","Sr","Y","Zr","Nb","Mo","Pb","Bi"]

#for coorelation coefficient - should be high
#x and y arrays of same length
#r = np.corrcoef(x,y)
#print(r)

#NRMSE - low is good
#RMSE = sqrt(MSE)
#RMSD/ (ymin-ymax)
#MSE = np.square(np.subtract(Y_true,Y_pred)).mean()
