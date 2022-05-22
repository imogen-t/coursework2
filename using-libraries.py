# %%
# https://www.learndatasci.com/glossary/binary-classification/
# https://stackabuse.com/classification-in-python-with-scikit-learn-and-pandas/

# imports

# graph plotting
import matplotlib.pyplot as plt
from matplotlib import cm

# read data into frames
import pandas as pd


# data analysis
import sklearn as sk
from sklearn.linear_model import LogisticRegression
from sklearn import svm
#%%
# read in training data

training = pd.read_csv("TrainingData.txt", sep=",",header=None)

# %%
""" 
Extract:
* Vector of outcomes for binary classification (normal or abnormal, 0 or 1)
* Matrix of explanatory variables (electricity cost at different times)

Both the vector and the matrix have a row for each training data point (10,000)
Matrix x Vector gives the original training data
"""

y_train = training.iloc[:,24]
X_train = training.iloc[:,:24]

# %%
"""
Logistic regression
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
* Limited-memory BFGS solver
* l2 penalty
* no random state
* max of 100 iterations
"""

model = LogisticRegression();
model.fit(X_train, y_train)

# %%
# Read in test data

X_test = pd.read_csv("TestingData.txt", sep=",",header=None)


# %%
# predict on test data

predictions = model.predict(X_test)

# %%
# Test accuracy of model 
# Cannot do this without labels for test data

print("Accuracy Test")
"""
Ideal accuracy test

Calculate number of:
* True positives
* False positives
* True negatives
* False negatives

accuracy = (TP+TN)/(TP+FP+TN+FN)
"""

# %%

# Select test points noted as abnormal

# insert predictions to training data
X_test.insert(24, 'prediction', predictions)


# %%
# Extract test points model labels as abnormal

abnormal_test = []

for index,row in X_test.iterrows():
    if(row.prediction == 1.0):
        abnormal_test.append(row)
# %%