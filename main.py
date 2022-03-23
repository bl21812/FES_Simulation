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

# import warnings
# warnings.filterwarnings("ignore")

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
  taThetaMuscleTendonLength = math.radians(90) # angle @ standing
  taMomentArm = 0.04
  taInsertion = np.transpose(np.array([0.06, -0.03]))
  taOrigin = np.transpose(np.array([0.3, -0.03]))
  taPennationAngle = math.radians(10)
  
  # Healthy Gait Model 
  # taHealthyActivation = lambda theta: 0 if theta < math.radians(90) else 1 # will modify
  # taHealthyActivation = lambda theta: 12/5 * theta - 14/15 # testing linear function
  taHealthyActivation = lambda theta: 0.4 
  
  tibialis = HillTypeMuscleModel(
    f0m = taF0m, 
    theta = taThetaMuscleTendonLength, 
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationFunc = taHealthyActivation,
    pennation = taPennationAngle
  )
 
  initialState = [ math.radians(145), 0, 1] # start at 40 degrees from standing
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

  taMoments = []
  for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
    taMuscleTendonLength = tibialis.muscleTendonLength(theta)
    taMoments.append(tibialis.momentArm * tibialis.getForce(taMuscleTendonLength, taNormMuscleLength))

  plotOutput(time, thetas, taMoments, "tibialis anterior", "green", "healthy")
  
  # FES Gait Model w/ sEMG signals
  # taActivation = fesModel.genEMG('constant', {'a': 0.1}, f) # will modify