import sys
import math
import numpy as np
import pandas as pd

from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from helpers.regression import forceVelocityRegression, forceLengthRegression, angleTorqueRegression

from plot import plotOutput
from model import model
from activations.healthy import healthy
from activations.fes import FES
from pid import PID
from simulate import simulate

import warnings
# warnings.filterwarnings("ignore")

print(sys.version)

# simulation time span
simTimeLower = 0 
simTimeUpper = 5

# initial angle of simulation (deg)
initAngle = 110

if __name__ == "__main__":
  # ---------------------------------------------------------------------
  # Setup

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
  tibialis = HillTypeMuscleModel(
    f0m = taF0m, 
    theta = taThetaMuscleTendonLength, 
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationModel = healthyModel,
    pennation = taPennationAngle
  )
 
  musclesHealthy = [tibialis]
  f = lambda t, x : model(x, musclesHealthy, regressionModels, t)
  time, thetas, allMuscleNormLengths = simulate(f, initAngle, simTimeUpper, simTimeLower)

  allMoments = []
  for muscle, muscleNormLengths in zip(musclesHealthy, allMuscleNormLengths):
    moments = []
    for theta, normMuscleLength in zip(thetas, muscleNormLengths):
      muscleTendonLength = muscle.muscleTendonLength(theta)
      moments.append(-muscle.momentArm * muscle.getForce(muscleTendonLength, normMuscleLength))
    allMoments.append(moments)

  taMoments = allMoments[0]
  plotOutput(time, thetas, taMoments, "tibialis anterior", "green", "healthy-linear-act")

  # ---------------------------------------------------------------------
  # FES Gait Model w/ sEMG signals

  # permuations of different input signals
  fesModels = []

  # types = ['sin', 'cos']
  # amplitudes = [0.1, 0.5, 1, 5, 10]
  # freqs = [1, 100, 250, 500]

  types = ['sin', 'cos']
  amplitudes = [0.1, 1, 10]
  freqs = [1, 100, 500]

  for a in amplitudes:
    for type in types:
      for freq in freqs:
        fesModel = FES()
        fesModel.genEMG(
          type = type, 
          params = {'a': a * 10**-3, 'b': freq}, 
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
    musclesFES = [tibialisFES]
    f = lambda t, x : model(x, musclesFES, regressionModels, t)
    time, thetas, allMuscleNormLengths = simulate(f, initAngle, simTimeUpper, simTimeLower)

    allMoments = []
    for muscle, muscleNormLengths in zip(musclesFES, allMuscleNormLengths):
      moments = []
      for theta, normMuscleLength in zip(thetas, muscleNormLengths):
        muscleTendonLength = muscle.muscleTendonLength(theta)
        moments.append(-muscle.momentArm * muscle.getForce(muscleTendonLength, normMuscleLength))
      allMoments.append(moments)
        
    taMoments = allMoments[0]
    plotOutput(time, thetas, taMoments, "tibialis anterior", "green", name)


  # ---------------------------------------------------------------------
  # PID FES Gait Model 
  p = 1
  i = 1
  d = 1

  healthyGaitPath = "scaled_images/healthy-linear-act.csv"
  df = pd.read_csv(healthyGaitPath)

  times = df["time"]
  times = [float(t) for t in times]

  thetas = df["theta"]
  thetas = [float(theta) for theta in thetas]
  
  pid = PID(
    p = p,
    i = i,
    d = d,
    target = [times, thetas],
    initState = math.radians(initAngle)
  )
  act = pid.update()
