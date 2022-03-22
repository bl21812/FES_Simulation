import sys
import math
import matplotlib.pyplot as plt
from scipy import integrate

from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from fes import *
from model import model
print(sys.version)

# simulation time span
simTimeLower = 0 
simTimeUpper = 5 
rtol = 10**-6
atol = 10**-8
if __name__ == "__main__": 
  fesModel = FES()

  # TA constants
  taF0m = 1
  taRestingMuscleLength = 1
  taRestingTendonLength = 1
  taMomentArm = 1
  taInsertion = np.transpose([0.06, -0.03])
  taOrigin = np.transpose(np.array([0.3, -0.03]))
  
  # Healthy Gait Model w/ constant activation 
  taHealthyActivation = lambda: 0.1 # will modify
  
  tibialis = HillTypeMuscleModel(
    f0m = taF0m, 
    restingMuscleLength = taRestingMuscleLength,
    restingTendonLength = taRestingTendonLength,
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationFunc = taHealthyActivation
  )
 
  initialState = [math.pi/2, 0, 1]
  f = lambda t, x : model(x, [tibialis])
  output = integrate.solve_ivp( # uses RK45 by default
    fun = f,
    t_span = (simTimeLower, simTimeUpper),
    y0 = initialState, # initial condition
    rtol = rtol,
    atol = atol
  )

  time = output.t
  y = output.y 
  thetas = y[0]
  taMuscleNormLengths = y[2]

  a = [1, 2, 3]
  b = [4, 5, 6]

  taMoments = []
  for theta, taNormMuscleLength in zip(thetas, taMuscleNormLengths):
    taMuscleTendonLength = tibialis.muscleTendonLength(theta)
    taMoments.append(tibialis.momentArm * tibialis.getForce(taMuscleTendonLength, taNormMuscleLength))

  fig, axs = plt.subplots(2)
  axs[0].plot(time, thetas)
  axs[0].set(xlabel = "Time (s)", ylabel = "Theta (rad)")
  
  axs[1].set(xlabel =  "Time (s)", ylabel = "Torques (Nm)")
  axs[1].plot(time, taMoments, 'tab:green')

  plt.show()
    
  

  print(y)
  # FES Gait Model w/ sEMG signals
  # taActivation = fesModel.genEMG('constant', {'a': 0.1}, f) # will modify

