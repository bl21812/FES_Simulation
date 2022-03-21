import numpy as np
import math
from sklearn.linear_model import Ridge
from helpers.constants import dataForceVelocity

def forceVelocityMuscle(vm) -> list:
  '''
  @param data: array-like structure in the form [velocity, force] used for training a model
  @param vm: muscle (contractile element) velocity) 
  
  returns force-velocity scale factor
  '''
  if len(vm) > 1 and len(vm[1]) > len(vm[0]):
    vm = np.array(vm).transpose()

  xs = [x[0] for x in dataForceVelocity]
  ys = [x[1] for x in dataForceVelocity]
  data = [xs, ys]
  # train Ridge model then use model weights to predict vm
  model = forceVelocityRegression(data)
  return modelEval(vm, model.coef_, model.intercept_)

def forceVelocityRegression(data):
  '''
  @param data: array-like structure in the form [length, force]. used for training.

  returns the ridge regression model fitted on data
  '''
  velocities, forces = data
  velocities, forces = np.array(velocities), np.array(forces)

  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(velocities, i, 0.15))

  x = np.array(x)
  x = np.reshape(x, (23, 5))

  # create a Ridge model with regularization param = 1
  model = Ridge(fit_intercept = False, alpha=1)
  model.fit(x, forces) # train the model

  # return ridge coefficients
  return model

def modelEval(input, ridge_coeff, intercept):
  '''
  Assume sigmoid type. 
  Helper function to create predictions using coefficients from a ridge model.
  Returns a scalar.
  '''
  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(input, i, 0.15))

  x = np.array(x)
  x = np.squeeze(x)
    
  return intercept + x.dot(ridge_coeff)

def sigmoid(x, mu, sigma): 
  exp_term = np.divide(-(x-mu), sigma) 
  return np.divide(1,(1 + np.exp(exp_term)))