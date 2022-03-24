import numpy as np
from sklearn.linear_model import Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from helpers.constants import dataForceVelocity, dataForceLength, dataAngleTorque, dataAngleTorque2

def forceLengthRegression():
  '''
  returns a Gaussian model that can be used to make predictions
  '''
  lengths = [x[0] for x in dataForceLength]
  forces = [x[1] for x in dataForceLength]
  lengths, forces = np.array(lengths), np.array(forces)

  # normalize the forces and the lengths using the index of the max force
  normForces = (forces - np.min(forces))/(np.max(forces) - np.min(forces)) 
  normLengths = lengths/lengths[np.argmax(forces)]

  regressionModel = GaussianProcessRegressor()

  # fit on the normalized data
  regressionModel.fit(np.reshape(normLengths, (-1, 1)), np.reshape(normForces, (-1,1))) 

  return regressionModel

def forceVelocityRegression():
  '''
  returns the ridge regression model fitted on data
  '''
  # dataForceVelocity is an array-like structure in the form [velocity, force] used for training a model
  velocities = np.array([x[0] for x in dataForceVelocity])
  forces = np.array([x[1] for x in dataForceVelocity])

  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(velocities, i, 0.15))

  x = np.array(x)
  x = np.reshape(x, (len(forces), len(x)))

  # create a Ridge model with regularization param = 1
  model = Ridge(alpha=1)
  model.fit(x, forces) # train the model

  return model

def angleTorqueRegression():
  angles = np.array([x[0] for x in dataAngleTorque2])
  torques = np.array([x[1] for x in dataAngleTorque2])

  x = []
  stdDev = np.std(angles)
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(angles, i, stdDev))
    
  x = np.array(x)
  x = np.reshape(x, (len(torques), len(x)))
  
  model = Ridge(alpha=1)
  model.fit(x, torques)

  return model

def modelEval(input, ridgeCoeff, intercept, sigma):
  '''
  Assume sigmoid type. 
  Helper function to create predictions using coefficients from a ridge model.
  Returns a scalar.
  '''
  x = []
  for i in np.arange(-1, -0.1, 0.2):
    x.append(sigmoid(input, i, sigma))

  x = np.array(x)
  x = np.squeeze(x)
    
  return intercept + x.dot(ridgeCoeff)
  
def sigmoid(x, mu, sigma): 
  expTerm = np.divide(-(x-mu), sigma)
  sigmoid = np.divide(1,(1 + np.exp(expTerm)))
    
  return sigmoid
  