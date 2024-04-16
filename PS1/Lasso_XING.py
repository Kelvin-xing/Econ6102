## import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import zipfile
from datetime import datetime
from dateutil.relativedelta import relativedelta


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from statsmodels.regression.linear_model import OLS

# ploting initiation
import matplotlib.pyplot as plt
sns.set_style("darkgrid")
pd.plotting.register_matplotlib_converters()
%matplotlib inline

FF5 = pd.read_csv('data/FF5_2000_2022.csv')
CRSP = pd.read_csv('data/CRSP_2000_2022.csv')
PS = pd.read_csv('data/PS_2000_2022.csv')
HXZ5 = pd.read_csv('data/HXZ5_2000_2022.csv')