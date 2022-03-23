import sys
import math
import os
import numpy as np

from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from helpers.regression import forceVelocityRegression, forceLengthRegression, angleTorqueRegression

from plot import plotOutput
from model import model
from activations.healthy import healthy
from activations.fes import FES
from simulate import simulate

import warnings
warnings.filterwarnings("ignore")

print(sys.version)

# simulation time span
simTimeLower = 0 
simTimeUpper = 5

if __name__ == "__main__": 
  if not os.path.exists("images"):
    os.mkdir("images")

  # first get the models
  forceVelocityRegressionModel = forceVelocityRegression()
  forceLengthRegressionModel = forceLengthRegression()
  angleTorqueRegressionModel = angleTorqueRegression()

  # create activation models
  healthyModel = healthy(muscleActivation = 1)
  fesModel = FES()

  # TA constants
  taF0m = 600
  taThetaMuscleTendonLength = math.radians(90) # angle @ standing
  taMomentArm = 0.04
  taInsertion = np.array([0.06, -0.03])
  taOrigin = np.array([0.3, -0.03])
  taPennationAngle = math.radians(10)

  # ---------------------------------------------------------------------
  # Healthy Gait Model
  tibialis = HillTypeMuscleModel(
    f0m = taF0m, 
    theta = taThetaMuscleTendonLength, 
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationModel = healthyModel,
    pennation = taPennationAngle
  )
 
  f = lambda t, x : model(x, [tibialis], forceLengthRegressionModel, forceVelocityRegressionModel, angleTorqueRegressionModel)
  time, thetas, taMuscleNormLengths = simulate(f, tibialis, simTimeUpper, simTimeLower)

  taMoments = []
  for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
    taMuscleTendonLength = tibialis.muscleTendonLength(theta)
    taMoments.append(tibialis.momentArm * tibialis.getForce(taMuscleTendonLength, taNormMuscleLength))

  plotOutput(time, thetas, taMoments, "tibialis anterior", "green", "healthy")

  # ---------------------------------------------------------------------
  # FES Gait Model w/ sEMG signals
  taActivation = fesModel.genEMG(
    type = 'const', 
    params = {'a': 0.1}, 
    freq = 100,
    simTime = simTimeUpper
  )
  
  tibialisFES = HillTypeMuscleModel(
    f0m = taF0m, 
    theta = taThetaMuscleTendonLength, 
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationModel = fesModel,
    pennation = taPennationAngle
  )

  f = lambda t, x : model(x, [tibialisFES], forceLengthRegressionModel, forceVelocityRegressionModel, angleTorqueRegressionModel)

