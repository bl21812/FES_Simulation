import sys
import math
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
  y = integrate.RK45(
    fun = f,
    t0 = simTimeLower, # initial state
    y0 = initialState, # initial condition
    t_bound = simTimeUpper,
    rtol = rtol,
    atol = atol
  )
  # FES Gait Model w/ sEMG signals
  # taActivation = fesModel.genEMG('constant', {'a': 0.1}, f) # will modify

