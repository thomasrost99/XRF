import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

answerA = pd.read_csv("/AnswerKeys/DataSet1/U1456A_XRF_calibrations.csv")
answerC = pd.read_csv("/AnswerKeys/DataSet1/U1456C_XRF_calibrations.csv")
answerUs = pd.read_csv("/AnswerKeys/DataSet1/U1456_our_calculation_standard_regression.csv")

#for coorelation coefficient - should be high
#x and y arrays of same length
#r = np.corrcoef(x,y)
#print(r)

#NRMSE - low is good
#RMSE = sqrt(MSE)
#RMSD/ (ymin-ymax)
#MSE = np.square(np.subtract(Y_true,Y_pred)).mean()
