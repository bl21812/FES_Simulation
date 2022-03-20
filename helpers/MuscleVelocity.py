import numpy as np
import math
from ForceLengthFunctions import forceLengthMuscle, forceLengthParallel
from ForceVelocityFunctions import forceVelocityMuscle
from scipy.optimize import fsolve

def getMuscleVelocity(a, lm, lt) -> list:
'''
@param a: activation (between 0 and 1)
@param lm: normalized length of muscle (contractile element)
@param lt: normalized length of tendon (series elastic element)

returns normalized lengthening velocity of muscle (contractile element)
'''
beta = 0.1 # damping coefficient (Millard et al.)
alpha = 0
f0M = 1

# vm is the velocity of the CE element (muscle)
func = lambda vm : f0M * (a * forceLengthMuscle(lm) * forceVelocityMuscle(vm) + forceLengthParallel(lm) + beta * vm) * math.cos(alpha) - f0m * forceLengthTendon(lt)

vm_initial = 0 # initial condition of the velocity
root = fsolve(func, vm_initial) # find the roots of the function 

return root
