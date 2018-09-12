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

path = r"E:\SV文件\surface.xls"
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


data = xlrd.open_workbook(r'E:\SV文件\surface.xls')
table = data.sheets()[0]
nrows = table.nrows-1
ncols = table.ncols-1

print(nrows)
print(ncols)
matrix = np.zeros((nrows,ncols))

for i in range(nrows):
    for j in range(ncols):
            matrix[i,j] = float(table.cell_value(i+1,j+1))

#print(matrix)
RACC = matrix[:, 0]
ACC = matrix[:, 1]
B_factor = matrix[:, 2]


from scipy import stats

for i in range(40):
    r_racc = stats.pearsonr(RACC,matrix[:, 3+i])[0]
    r_acc = stats.pearsonr(ACC,matrix[:, 3+i])[0]
    r_b_factor = stats.pearsonr(B_factor,matrix[:, 3+i])[0]

    p_racc = stats.pearsonr(RACC,matrix[:, 3+i])[1]
    p_acc = stats.pearsonr(ACC,matrix[:, 3+i])[1]
    p_b_factor = stats.pearsonr(B_factor,matrix[:, 3+i])[1]

    excel_write(915, 4 + i, r_racc)
    excel_write(916, 4 + i, r_acc)
    excel_write(917, 4 + i, r_b_factor)

    excel_write(919, 4 + i, p_racc)
    excel_write(920, 4 + i, p_acc)
    excel_write(921, 4 + i, p_b_factor)



