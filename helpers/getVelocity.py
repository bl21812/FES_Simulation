import numpy as np
from sklearn.preprocessing import normalize

def getVelocity(a, lm, lt) -> list:
'''
@param a: activation (between 0 and 1)
@param lm: normalized length of muscle (contractile element)
@param lt: normalized length of tendon (series elastic element)

returns normalized lengthening velocity of muscle (contractile element)
'''
beta = 0.1 # damping coefficient (Millard et al.)
alpha = 0
foM = 1

# WRITE CODE HERE TO CALCULATE VELOCITY
  y = root foM*(a*forceLength(lm)*forcevelocity(root) + forceLength(lm) + beta*root)*cos(alpha) - foM*forceLength(lt)
  vm0 = 0
  root = fzero(y,vm0)

return
