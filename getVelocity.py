import numpy as np
from sklearn.preprocessing import normalize

def getVelocity(a, lm, lt) -> list:

# Input Parameters
# a: activation (between 0 and 1)
# lm: normalized length of muscle (contractile element)
# lt: normalized length of tendon (series elastic element)

# Output
# root: normalized lengthening velocity of muscle (contractile element)

# damping coefficient (see damped model in Millard et al.)
  beta = 0.1
  alpha = 0
  foM = 1

# WRITE CODE HERE TO CALCULATE VELOCITY
  y = root foM*(a*forceLength(lm)*forcevelocity(root) + forceLength(lm) + beta*root)*cos(alpha) - foM*forceLength(lt)
  vm0 = 0
  root = fzero(y,vm0)

return
