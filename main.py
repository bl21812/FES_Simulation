import sys
import math
import os
import numpy as np
import csv

from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from helpers.regression import forceVelocityRegression, forceLengthRegression, angleTorqueRegression

from plot import plotOutput
from model import model
from activations.healthy import healthy
from activations.fes import FES
from simulate import simulate

import warnings
# warnings.filterwarnings("ignore")

print(sys.version)

# simulation time span
simTimeLower = 0 
simTimeUpper = 50

if __name__ == "__main__": 
  if not os.path.exists("images"):
    os.mkdir("images")

  # first get the models
  forceVelocityRegressionModel = forceVelocityRegression()
  forceLengthRegressionModel = forceLengthRegression()
  angleTorqueRegressionModel = angleTorqueRegression()

  regressionModels = [forceLengthRegressionModel, forceVelocityRegressionModel, angleTorqueRegressionModel]
  # create healthy models
  healthyModel = healthy(muscleActivation = 1)

  # TA constants
  taF0m = 600
  taThetaMuscleTendonLength = math.radians(90) # angle @ standing
  taMomentArm = 0.04
  taInsertion = np.array([0.06, -0.03])
  taOrigin = np.array([0.3, -0.03])
  taPennationAngle = math.radians(10)

  # ---------------------------------------------------------------------
  # Healthy Gait Model
  # tibialis = HillTypeMuscleModel(
  #   f0m = taF0m, 
  #   theta = taThetaMuscleTendonLength, 
  #   insertion = taInsertion,
  #   origin = taOrigin, 
  #   momentArm = taMomentArm,
  #   activationModel = healthyModel,
  #   pennation = taPennationAngle
  # )
 
  # f = lambda t, x : model(x, [tibialis], regressionModels, t)
  # time, thetas, taMuscleNormLengths = simulate(f, tibialis, simTimeUpper, simTimeLower)

  # taMoments = []
  # for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
  #   taMuscleTendonLength = tibialis.muscleTendonLength(theta)
  #   taMoments.append(tibialis.momentArm * tibialis.getForce(taMuscleTendonLength, taNormMuscleLength))

  # plotOutput(time, thetas, taMoments, "tibialis anterior", "green", "healthy-linear-act")

  # ---------------------------------------------------------------------
  # FES Gait Model w/ sEMG signals

  # permutations of activation with b constant (no vert shift)
  fesModels = []
  b = 0
  types = ['sin', 'cos']
  activations = [0.1, 0.5, 1, 5, 10]
  freqs = [1, 100, 250, 500]
  
  for type in types:
    for a in activations:
      for freq in freqs:
        fesModel = FES()
        fesModel.genEMG(
          type = type, 
          params = {'a': a, 'b': freq}, 
          freq = freq,
          simTime = simTimeUpper
        )
        fesModels.append((fesModel, f"{type}-{a}-{freq}"))

  for fesModel, name in fesModels:
    tibialisFES = HillTypeMuscleModel(
      f0m = taF0m, 
      theta = taThetaMuscleTendonLength, 
      insertion = taInsertion,
      origin = taOrigin, 
      momentArm = taMomentArm,
      activationModel = fesModel,
      pennation = taPennationAngle
    )
    f = lambda t, x : model(x, [tibialisFES], regressionModels, t)
    time, thetas, taMuscleNormLengths = simulate(f, tibialisFES, simTimeUpper, simTimeLower)

    taMoments = []
    for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
      taMuscleTendonLength = tibialisFES.muscleTendonLength(theta)
      taMoments.append(tibialisFES.momentArm * tibialisFES.getForce(taMuscleTendonLength, taNormMuscleLength))
      
    plotOutput(time, thetas, taMoments, "tibialis anterior", "green", name)

