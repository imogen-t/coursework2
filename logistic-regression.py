# %%
import numpy as np 
import pandas as pd 
from sklearn import preprocessing

# %%
# Import training data and split to explainatory variables and outcomes

df = pd.read_csv('TrainingData.txt', header=None)

X_train = df.iloc[:,:24]
y_train = df.iloc[:,24:]

X_train = preprocessing.scale(X_train)

X_test = pd.read_csv('TestingData.txt', header=None)

X_test = preprocessing.scale(X_test)

# %%
# Sigmoid
def sigmoid(z):
    out = 1/(1+np.exp(-z))
    return out 

# %%
# Learning optimal weights and bias
def optimise(x, y,parameters,learning_rate=0.02,iterations=1000): 
    size = x.shape[0]
    weight = parameters["weight"] 
    bias = parameters["bias"]

    # iterate over data to aim for convergence in gradient descent
    for i in range(iterations): 
        # calculate loss
        sigma = sigmoid(np.dot(x, weight) + bias)
        loss = -1/size * np.sum(y * np.log(sigma)) + (1 - y) * np.log(1-sigma)
        # parameter update scalars
        dW = 1/size * np.dot(x.T, (sigma - y))
        db = 1/size * np.sum(sigma - y)
        # update parameters
        weight -= learning_rate * dW
        bias -= learning_rate * db 
    
    parameters["weight"] = weight
    parameters["bias"] = bias
    return parameters

# %%
# Initialise weight and bias to 0s

init_parameters = {}
init_parameters["weight"] = np.zeros(X_train.shape[1])
init_parameters["bias"] = 0

# %% 
# Train the model

training = optimise(X_train, y_train[24], parameters=init_parameters)

X_testdf = pd.DataFrame(X_test)
out = np.dot(X_test,training["weight"]+training["bias"])
sig = sigmoid(out) >= 1/2 # false => 0; true => 1

predictions = pd.DataFrame(sig) 

X_testdf['prediction'] = predictions

abnormals = X_testdf.loc[X_testdf['prediction']]

# write outcomes to .csv files

abnormals.to_csv('nonlibrary-abnormals.csv', header=None)

params = pd.DataFrame.from_dict(init_parameters)
params.to_csv('nonlibrary-parameters.csv')
# %%
