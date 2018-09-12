from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from scipy import stats
from scipy.stats import ttest_rel
import pandas
import numpy as np

import os
import xlrd
import xlwt
import re
import numpy
import math
from xlutils.copy import copy

from sklearn.model_selection import ShuffleSplit
import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold

import xlrd
from  sklearn import  cross_validation
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split


from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold

import xlrd
import numpy as np
from  sklearn import  cross_validation
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation, metrics
from xlrd import open_workbook

path = r"E:\SV文件\sv_cx - 副本.xls"
def excel_write(row, column, content):
    rb = open_workbook(path)
    # 复制
    wb = copy(rb)
    # 选取表单
    s = wb.get_sheet(0)
    # 写入数据
    s.write(row, column, content)
    # 保存
    wb.save(path)


data = xlrd.open_workbook(r'E:\SV文件\sv_cx.xls')
table = data.sheets()[0]
nrows = table.nrows-1
ncols = table.ncols-1

# print(nrows)
# print(ncols-1)
matrix = np.zeros((nrows,ncols))

for i in range(nrows):
    for j in range(ncols):
            matrix[i,j] = float(table.cell_value(i+1,j+1))

X_train = preprocessing.scale(matrix[:,0])


i = 1
for num in X_train:
    excel_write(i,1, num)
    i = i + 1

X_train = preprocessing.scale(matrix[:,1])

i = 1
for num in X_train:
    excel_write(i,2, num)
    i = i + 1

X_train = preprocessing.scale(matrix[:,2])

i = 1
for num in X_train:
    excel_write(i,3, num)
    i = i + 1

X_train = preprocessing.scale(matrix[:,3])

i = 1
for num in X_train:
    excel_write(i,4, num)
    i = i + 1
