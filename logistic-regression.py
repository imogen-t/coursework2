# %%
import numpy as np 
import pandas as pd 
import random

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
    return out >= 1/2

# %%
# Optimise
def optimise(x, y,parameters,learning_rate=0.02,iterations=500): 
    size = x.shape[0]
    weight = parameters["weight"] 
    bias = parameters["bias"]


    for i in range(iterations): 
        sigma = sigmoid(np.dot(x, weight) + bias)
        loss = -1/size * np.sum(y * np.log(sigma)) + (1 - y) * np.log(1-sigma)
        dW = 1/size * np.dot(x.T, (sigma - y))
        db = 1/size * np.sum(sigma - y)
        weight -= learning_rate * dW
        bias -= learning_rate * db 
    
    parameters["weight"] = weight
    parameters["bias"] = bias
    return parameters

# %%
# Initialise weight and bias to 0 values
## can play with the effects of small random values

init_parameters = {}
init_parameters["weight"] = np.zeros(X_train.shape[1])
init_parameters["bias"] = random.uniform(-0.1,0.1)


# %% 
# Train the model


training = optimise(X_train, y_train[24], parameters=init_parameters)

y_train_hat = np.dot(X_test,training["weight"]+training["bias"])

predictions = sigmoid(y_train_hat)



# %%
