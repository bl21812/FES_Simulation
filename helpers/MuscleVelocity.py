import math
from helpers.ForceLengthFunctions import forceLengthMuscle, forceLengthParallel, forceLengthTendon
from helpers.ForceVelocityFunctions import forceVelocityMuscle
from scipy.optimize import fsolve

def getMuscleVelocity(a, lm, lt, alpha, forceLengthRegressionModel, forceVelocityRegressionModel):
  '''
  @param a: activation (between 0 and 1)
  @param lm: normalized length of muscle (contractile element) -> scalar value
  @param lt: normalized length of tendon (series elastic element) -> scalar value
  @param alpha: pennation angle of the muscle
  @param forceLengthRegressionModel: trained model to use in forceLengthMuscle
  @param forceVelocityRegressionModel: trained model to use in forceVelocityMuscle
  
  returns normalized lengthening velocity of muscle (contractile element)
  '''
  beta = 0.1 # damping coefficient (Millard et al.)
  f0m = 1
  
  # vm is the velocity of the CE element (muscle)
  func = lambda vm : f0m * (a * forceLengthMuscle(forceLengthRegressionModel, lm) * forceVelocityMuscle(forceVelocityRegressionModel, vm) + forceLengthParallel(lm) + beta * vm) * math.cos(alpha) - f0m * forceLengthTendon(lt)
  
  vmInitial = 0 # initial condition of the velocity
  root = fsolve(func, vmInitial) # find the roots of the function 
  
  return root
