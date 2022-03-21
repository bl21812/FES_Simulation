import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor

from helpers.constants import dataForceLength

def forceLengthTendon(lt):
  ''' 
  Determine force produced by series elastic element

  @param lt: normalized length of series elastic elements
  '''     
  return 10 * (lt-1) + 240 * (lt-1)**2 if lt >= 1 else 0

def forceLengthParallel(lm):
  ''' 
  Determine normalized force produced by contractile element

  @param lm: normalized length of contractile elements
  ''' 
  return (3 * (lm - 1)**2)/(0.6 + lm - 1) if lm >= 1 else 0


def forceLengthMuscle(normMuscleLength):
  '''
  Determine force-length scale factors

  @param normMuscleLength: normalized length of contractile elements
  '''
  xs = [x[0] for x in dataForceLength]
  ys = [x[1] for x in dataForceLength]
  data = [xs, ys] # array-like structure in the form [length, force] used for training a model
  model = forceLengthRegression(data)
  return model.predict([[normMuscleLength]])[0]


def forceLengthRegression(data):
  '''
  Generate a Gaussian model
  
  @param data: array-like structure in the form [length, force]. used for training.

  returns a Gaussian model that can be used to make predictions
  '''
  lengths, forces = data
  lengths, forces = np.array(lengths), np.array(forces)

  # normalize the forces and the lengths using the index of the max force
  normForces = (forces - np.min(forces))/(np.max(forces) - np.min(forces)) 
  normLengths = lengths/lengths[np.argmax(forces)]

  regressionModel = GaussianProcessRegressor()

  # fit on the normalized data
  regressionModel.fit(np.reshape(normLengths, (-1, 1)), np.reshape(normForces, (-1,1))) 

  return regressionModel
