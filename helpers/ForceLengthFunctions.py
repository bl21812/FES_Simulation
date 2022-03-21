import numpy as np
import sklearn

from helpers.constants import dataForceLength

def forceLengthTendon(normTendonLengths) -> list:
  ''' 
  Determine normalized force produced by series elastic element

  @param normTendonLengths: list of normalized lengths of series eleastic elements
  '''  
  normForces = []
  for lt in normTendonLengths:
    forceTendon = 10 * (lt-1) + 240 * (lt-1)**2 if lt >= 1 else 0
    normForces.append(forceTendon)
    
  return normForces

def forceLengthParallel(normMuscleLengths) -> list:
  ''' 
  Determine normalized force produced by contractile element

  @param normMuscleLengths: list of normalized lengths of contractile elements
  ''' 
  normForces = []
  for lm in normMuscleLengths:
    forceMuscle  = (3 * (lm - 1)^2)/(0.6 + lm - 1) if lm >= 1 else 0
    normForces.append(forceMuscle)
    
  return normForces


def forceLengthMuscle(normMuscleLengths) -> list:
  '''
  Determine force-length scale factors

  @param normMuscleLengths: list of normalized lengths of contractile elements
  '''
  # TODO: format data in the right way
  data = dataForceLength # array-like structure in the form [length, force] used for training a model
  model = forceLengthRegression(data)
  return model.predict(normMuscleLengths)


def forceLengthRegression(data):
  '''
  Generate a Gaussian model
  
  @param data: array-like structure in the form [length, force]. used for training.

  returns a Gaussian model that can be used to make predictions
  '''
  lengths, forces = data

  # normalize the forces and the lengths using the index of the max force
  normForces = (forces - np.min(forces))/(np.max(forces) - np.min(forces)) 
  normLengths = lengths/lengths[np.argmax(forces)]

  regressionModel = sklearn.gaussian_process.GaussianProcessRegressor()

  # fit on the normalized data
  regressionModel.fit(normLengths, normForces)

  return regressionModel
