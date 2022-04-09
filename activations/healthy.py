from activations.activation import activation
import math

class healthy(activation):
  def __init__(self, muscleActivation):
    self.muscleActivation = muscleActivation
    
  def getNextActivation(self, theta, t):
    # f = lambda x: -1/math.radians(40)*x + 11/4
    # f = lambda x: 1/math.radians(40)*x - 11/4
    # f = lambda x: -0.5/math.radians(40)*x + 15/8

    # f = lambda x: -1.2891550390444*x + 2.575

    # return t**2
    # f = lambda x: -0.71619724391353*x + 1.875
    # f = lambda x: 0.5/math.radians(40)*x - 15/8

    # f = lambda x: 0.5*math.cos(x-math.radians(70)) + 0.5

    # if theta < math.radians(70):
    #   return 1
    # elif theta > math.radians(110):
    #   return 0.1
    
    # return f(theta)
    # return f(t)
    return 0.1

    # return self.muscleActivation