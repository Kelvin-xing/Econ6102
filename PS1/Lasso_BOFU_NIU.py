import numpy as np
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from linearmodels.panel import PanelOLS
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
import sys
sys.path.append('/path/to/scikit-learn')




# Section 1: load the data

data_factor = pd.read_csv("D:/学习/研一/6102/作业1/Data-20240401/raw_data/data_factor.csv")

# Section 2: construct the lag factors

del data_factor['R_MKT']

data_factor = data_factor.rename(columns={'Mkt-RF': 'Mkt_RF'})

data_lasso = [[]for i in range(82060)]

n = len(data_factor)
print(n)

def fun(data1,data2,i,variable):
    data1[i].append(data2[variable][i])
    data1[i].append(data2[variable][i - 1])
    data1[i].append(data2[variable][i - 2])
    data1[i].append(data2[variable][i - 3])
    data1[i].append(data2[variable][i - 4])
    data1[i].append(data2[variable][i - 5])


for i in range(5, n):
    print(i)
    if data_factor['PERMNO'][i] == data_factor['PERMNO'][i-5]:
        data_lasso[i].append(data_factor['PERMNO'][i])
        data_lasso[i].append(data_factor['YYYYMM'][i])
        data_lasso[i].append(data_factor['MthRet'][i])
        fun(data_lasso,data_factor,i,'Mkt_RF')
        fun(data_lasso,data_factor,i,'SMB')
        fun(data_lasso, data_factor, i, 'HML')
        fun(data_lasso, data_factor, i, 'RMW')
        fun(data_lasso, data_factor, i, 'CMA')
        fun(data_lasso, data_factor, i, 'R_ME')
        fun(data_lasso, data_factor, i, 'R_IA')
        fun(data_lasso, data_factor, i, 'R_ROE')
        fun(data_lasso, data_factor, i, 'R_EG')
        fun(data_lasso, data_factor, i, 'AggLiq')
        fun(data_lasso, data_factor, i, 'eq8')
        fun(data_lasso, data_factor, i, 'LIQ_V')

data_lasso = pd.DataFrame(data_lasso)
data_lasso.columns = ['name','time','MthRet',
                        'Mkt_RF' ,'Mkt_RFl1' , 'Mkt_RFl2','Mkt_RFl3' ,'Mkt_RFl4', 'Mkt_RFl5',
           'SMB' ,'SMBl1', 'SMBl2', 'SMBl3', 'SMBl4','SMBl5',
           'HML','HMLl1','HMLl2','HMLl3','HMLl4','HMLl5',
           'RMW','RMWl1','RMWl2','RMWl3','RMWl4','RMWl5',
           'CMA ','CMAl1','CMAl2','CMAl3','CMAl4','CMAl5',
           'R_ME','R_MEl1','R_MEl2','R_MEl3','R_MEl4','R_MEl5',
           'R_IA','R_IAl1','R_IAl2','R_IAl3','R_IAl4','R_IAl5',
           'R_ROE','R_ROEl1','R_ROEl2','R_ROEl3','R_ROEl4','R_ROEl5',
           'R_EG','R_EGl1','R_EGl2','R_EGl3','R_EGl4','R_EGl5',
           'AggLiq','AggLiql1','AggLiql2','AggLiql3','AggLiql4','AggLiql5',
           'eq8','eq8l1','eq8l2','eq8l3','eq8l4','eq8l5',
           'LIQ_V','LIQ_Vl1','LIQ_Vl2','LIQ_Vl3','LIQ_Vl4','LIQ_Vl5']



data_lasso.to_csv("D:/学习/研一/6102/作业1/Data-20240401/data_lasso.csv")

#data_lasso在data_factor基础上增加了滞后项因子


