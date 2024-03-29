# -*- coding: utf-8 -*-
"""Visa-Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FHpg4enRK9C2TWNciixYvASd1lNqIgEQ
"""

! pip install kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download nsharan/h-1b-visa

! unzip "/content/h-1b-visa.zip"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, plot_confusion_matrix, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

df= pd.read_csv("/content/h1b_kaggle.csv")
df.head()
df.shape

df.head()

df = df[df['PREVAILING_WAGE'] <= 500000]

s0 = df.CASE_STATUS[df.CASE_STATUS.eq("CERTIFIED")].sample(85000).index
s1 = df.CASE_STATUS[df.CASE_STATUS.eq("CERTIFIED-WITHDRAWN")].sample(85000).index 
s2 = df.CASE_STATUS[df.CASE_STATUS.eq("DENIED")].sample(85000).index
s3 = df.CASE_STATUS[df.CASE_STATUS.eq("WITHDRAWN")].sample(85000).index 

samp = df.loc[s0.union(s1).union(s2).union(s3)]
samp.CASE_STATUS.value_counts()
df = samp

df.PREVAILING_WAGE.max()

df['SOC_NAME'] = df['SOC_NAME'].fillna(df['SOC_NAME'].mode()[0])
df.CASE_STATUS.value_counts()

df['CASE_STATUS'] = df['CASE_STATUS'].map({'CERTIFIED' : 0, 'CERTIFIED-WITHDRAWN' : 1, 'DENIED' : 2, 'WITHDRAWN' : 3, 'PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED' : 4, 'REJECTED' : 5, 'INVALIDATED' : 6})

df.head()

# def wage_categorization(wage):
#     if wage <=50000:
#         return "VERY LOW"
#     elif wage >50000 and wage <= 70000:
#         return "LOW"
#     elif wage >70000 and wage <= 90000:
#         return "MEDIUM"
#     elif wage >90000 and wage<=150000:
#         return "HIGH"
#     elif wage >=150000:
#         return "VERY HIGH"

# df['WAGE_CATEGORY'] = df['PREVAILING_WAGE'].apply(wage_categorization)

df['FULL_TIME_POSITION'] = df['FULL_TIME_POSITION'].map({'N' : 0, 'Y' : 1})
df.head()

import sys
df['SOC_NAME1'] = 'others'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('computer','software')] = 'it'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('chief','management')] = 'manager'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('mechanical')] = 'mechanical'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('database')] = 'database'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('sales','market')] = 'scm'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('financial')] = 'finance'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('public','fundraising')] = 'pr'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('education','law')] = 'administrative'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('auditors','compliance')] = 'audit'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('distribution','logistics')] = 'scm'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('recruiters','human')] = 'hr'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('agricultural','farm')] = 'agri'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('construction','architectural')] = 'estate'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('forencsic','health')] = 'medical'
df['SOC_NAME1'][df['SOC_NAME'].str.contains('teachers')] = 'education'

df = df.drop(['Unnamed: 0', 'EMPLOYER_NAME', 'SOC_NAME','JOB_TITLE','WORKSITE', 'lon','lat'], axis = 1)
df.head()

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df.SOC_NAME1)
# print list(le.classes_)
df['SOC_N']=le.transform(df['SOC_NAME1'])

df.head()

df = df.drop(['SOC_NAME1'], axis=1)

import seaborn as sns
sns.heatmap(df.corr(), annot=True, cmap="RdYlGn", annot_kws={"size":15})

df.columns









x = df.drop(['CASE_STATUS'], axis=1) # Independent variables
y = df['CASE_STATUS'] # Dependent variables

x.columns

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)



x_train_encode.head()

from sklearn.preprocessing import OneHotEncoder
x_train_encode = pd.get_dummies(x_train)
x_test_encode = pd.get_dummies(x_test)

x_test_encode.head()

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
LogReg = LogisticRegression()
LogReg.fit(x_train_encode, y_train)
y_pred_lg = LogReg.predict(x_test_encode)

print(classification_report(y_test, y_pred_lg))
plot_confusion_matrix(LogReg, x_test, y_test)
plt.title("Logistic Regression")
plt.show()

mlp = MLPClassifier(hidden_layer_sizes=(20,20,20,20,20), max_iter=1000)
mlp.fit(x_train_encode, y_train)
y_pred_mlp = mlp.predict(x_test_encode)
confusion = metrics.confusion_matrix(y_test, y_pred_mlp)
print(confusion)
print(metrics.classification_report(y_test, y_pred_mlp))
plot_confusion_matrix(mlp, x_test, y_test)
plt.title("MLP")
plt.show()



y_pred_mlp = mlp.predict(x_test_encode)

print(classification_report(y_pred_mlp, y_test))

plot_confusion_matrix(mlp, x_test, y_test)
plt.title("mlp")
plt.show()

rf = RandomForestClassifier(max_depth=10, random_state=42)
rf.fit(x_train_encode, y_train)


# scores
# scores_RF = cross_val_score(clf, x, y, cv=10)

# print('----------------cross validation---------------------')
# print(scores_RF) #cross validation
# print('------------------avg-------------------')
# print(scores_RF.mean()) #avg
# print('------------------classification_report-------------------')

y_pred_rf = rf.predict(x_test_encode)


print(classification_report(y_pred_rf, y_test))

plot_confusion_matrix(rf, x_test, y_test)
plt.title("Random forrest")
plt.show()

dt = DecisionTreeClassifier(random_state=42)

dt = dt.fit(x_train_encode, y_train)



y_pred_dt = dt.predict(x_test_encode)


print(classification_report(y_pred_dt, y_test))

plot_confusion_matrix(dt, x_test, y_test)
plt.title("Decision Tree")
plt.show()