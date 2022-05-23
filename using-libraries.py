# %%
# imports

# graph plotting
import matplotlib.pyplot as plt
from matplotlib import cm

# read data into frames
import pandas as pd

import numpy as np

# data analysis
import sklearn as sk
from sklearn.linear_model import LogisticRegression
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

model = LogisticRegression(max_iter=1000);
model.fit(X_train, y_train)

pd.DataFrame(model.coef_).to_csv('library-parameters.csv', header=None)

# %%
# Read in test data

X_test = pd.read_csv("TestingData.txt", sep=",",header=None)


# %%
# predict on test data

predictions = model.predict(X_test)

abnormal_count = np.count_nonzero(predictions == 1)

# %%

# Select test points noted as abnormal

# insert predictions to training data
X_test.insert(24, 'prediction', predictions)


# %%
# Extract test points model labels as abnormal

abnormals = X_test.loc[X_test['prediction']==1]
# %%
# write to csv

abnormals.to_csv('library-abnormals.csv', header=None)

X_test.to_csv('TestingResults.csv', header=None)
# %%
