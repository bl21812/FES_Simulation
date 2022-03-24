from activations.activation import activation
import math

class healthy(activation):
  def __init__(self, muscleActivation):
    self.muscleActivation = muscleActivation
    
  def getNextActivation(self, theta, _):
    f = lambda x: -1/math.radians(40) + 7/4
    return f(theta)