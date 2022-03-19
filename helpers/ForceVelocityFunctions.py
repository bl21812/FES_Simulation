import numpy as np
import sklearn

def forceVeloctiyMuscle(data, vm) -> list:
'''
@param data: array-like structure in the form [velocity, force] used for training a model
@param vm: muscle (contractile element) velocity) 

returns force-velocity scale factor
'''

  if len(vm[1]) > len(vm[0]):
    vm = np.array(vm).transpose()

  # TODO figure out how to run model_eval
  # global force_velocity_regression
  # force_velocity_scale_factor = model_eval('Sigmoid', vm, force_velocity_regression)

  coefficients = forceVelocityRegression(data)
  return modelEval(vm, coefficients)

def forceVelocityRegression(data):
  '''
  @param data: array-like structure in the form [length, force]. used for training.

  returns a ridge coefficients from a ridge regression model fitted on data
  '''
  
  velocities, forces = data
  velocities, forces = np.array(velocities), np.array(forces)

  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(velocities, i, 0.15))

  # TODO figure out the equivalent params in ridge and if this returns coefficients
  # force_velocity_regression = ridge(force, X, 1, 0);
  model = sklearn.linear_model.Ridge()
  model.fit(x, forces)

  return model

def modelEval(input, ridge_coeff):
  '''
  Assume sigmoid type. 
  '''
  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(input, i, 0.15))

  x = np.array(x)
    
  return ridge_coeff[0] + x.dot(ridge_coeff[1:])

def sigmoid(x, mu, sigma): 
  # TODO figure out how to do ./ operator
  # fun = @(x, mu, sigma) 1./(1+exp(-(x-mu)./sigma));
  return 1./(1+exp(-(x-mu)./sigma))