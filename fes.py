import numpy as np
import math

neuralActivations = []
class FES:

  def __init__(self, alpha, beta, A = 0.05):
    self.neural_activations = []

    A = 0.05
    
    a10 = 0.3085 + A * np.sin(math.pi/4)
    u0 = 0.3085 - A * np.cos(math.pi/4)
    m = (1 - a10) / (1 - u0)
    b = (a10 - u0) / (1 - u0)

    cFunc = lambda d : (math.exp(a10 / d) - 1) / u0
    derivCFunc = lambda d : d

  def getActivation(self, t):
    if 