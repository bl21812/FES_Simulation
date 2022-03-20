import sys
from constants import *
from helpers.HillTypeMuscleModel import HillTypeMuscleModel
from fes import *
print(sys.version)

if __name__ == "__main__": 
  # Healthy Gait Model
  # TODO
  taF0m = 1
  taRestingMuscleLength = 1
  taRestingTendonLength = 1
  taMomentArm = 1
  taHealthyGaitActivationFunc = lambda: 0.05
  
  taInsertion = np.transpose([0.06, -0.03])
  taOrigin = np.transpose(np.array([0.3, -0.03]))
  
  tibialis = HillTypeMuscleModel(
    f0m = tibialisF0m, 
    restingMuscleLength = taRestingMuscleLength,
    restingTendonLength = taRestingTendonLength,
    insertion = taInsertion,
    origin = taOrigin, 
    momentArm = taMomentArm,
    activationFunc = taHealthyGaitActivationFunc
  )

  # FES Model
  fesModel = FES()
