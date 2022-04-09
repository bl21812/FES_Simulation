from activations.activation import activation
import math

class healthy(activation):
  def __init__(self, muscleActivation):
    self.muscleActivation = muscleActivation
    
  def getNextActivation(self, theta, _):
    # f = lambda x: -1/math.radians(40)*x + 11/4
    # f = lambda x: 1/math.radians(40)*x - 11/4
    f = lambda x: -0.5/math.radians(40)*x + 15/8
    # f = lambda x: 0.5/math.radians(40)*x - 15/8
    return f(theta)
    # return f(_)
    # return 0.1

    return self.muscleActivation