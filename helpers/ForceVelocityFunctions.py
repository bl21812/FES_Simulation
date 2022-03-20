import numpy as np
import math
import sklearn

def forceVelocityMuscle(data, vm) -> list:
'''
@param data: array-like structure in the form [velocity, force] used for training a model
@param vm: muscle (contractile element) velocity) 

returns force-velocity scale factor
'''
  if len(vm[1]) > len(vm[0]):
    vm = np.array(vm).transpose()

  # train Ridge model then use model weights to predict vm
  coefficients = forceVelocityRegression(data)
  return modelEval(vm, coefficients)

def forceVelocityRegression(data) -> list:
  '''
  @param data: array-like structure in the form [length, force]. used for training.

  returns a ridge coefficients from a ridge regression model fitted on data
  '''
  velocities, forces = data
  velocities, forces = np.array(velocities), np.array(forces)

  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(velocities, i, 0.15))

  # create a Ridge model with regularization param = 1
  model = sklearn.linear_model.Ridge(alpha=1)
  model.fit(x, forces) # train the model

  # return ridge coefficients
  return model.coef_

def modelEval(input, ridge_coeff):
  '''
  Assume sigmoid type. 
  Helper function to create predictions using coefficients from a ridge model.
  '''
  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(input, i, 0.15))

  x = np.array(x)
    
  return ridge_coeff[0] + x.dot(ridge_coeff[1:])

def sigmoid(x, mu, sigma): 
  # Note: np.divide performs element-wise division 
  exp_term = np.divide(-(x-mu), sigma)
  return np.divide(1,(1 + math.exp(exp_term)))