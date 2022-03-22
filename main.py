import sys
import math
import os
import numpy as np
from scipy import integrate

from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from helpers.ForceVelocityFunctions import forceVelocityRegression
from helpers.ForceLengthFunctions import forceLengthRegression
from plot import plotOutput
from fes import FES
from model import model

print(sys.version)
  
if __name__ == "__main__": 
  if not os.path.exists("images"):
    os.mkdir("images")

  # simulation time span
  simTimeLower = 0 
  simTimeUpper = 5 
  
  # tolerances for simulation
  rtol = 10**-6
  atol = 10**-8

  # first train the models
  forceVelocityRegressionModel = forceVelocityRegression()
  forceLengthRegressionModel = forceLengthRegression()
  
  fesModel = FES()

  # TA constants
  taF0m = 600
  taStartingTheta = math.pi/2
  taMomentArm = 0.04
  taInsertion = np.transpose(np.array([0.06, -0.03]))
  taOrigin = np.transpose(np.array([0.3, -0.03]))
  
  # Healthy Gait Model w/ constant activation 
  taHealthyActivation = lambda: 0.4 # will modify
  
  tibialis = HillTypeMuscleModel(
    f0m = taF0m, 
    theta = taStartingTheta, 
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationFunc = taHealthyActivation
  )
 
  initialState = [math.pi/2, 0, 1]
  f = lambda t, x : model(x, [tibialis], forceLengthRegressionModel, forceVelocityRegressionModel)
  output = integrate.solve_ivp( # uses RK45 by default
    fun = f,
    t_span = (simTimeLower, simTimeUpper),
    y0 = initialState, # initial condition
    rtol = rtol,
    atol = atol
  )

  time, y = output.t, output.y
  thetas, _, taMuscleNormLengths = y

  print(time, y)
  taMoments = []
  for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
    taMuscleTendonLength = tibialis.muscleTendonLength(theta)
    taMoments.append(tibialis.momentArm * tibialis.getForce(taMuscleTendonLength, taNormMuscleLength))

  plotOutput(time, thetas, taMoments, "tibialis anterior", "green", "healthy")
  
  # FES Gait Model w/ sEMG signals
  # taActivation = fesModel.genEMG('constant', {'a': 0.1}, f) # will modify