from activations.activation import activation
import math

class healthy(activation):
  def __init__(self, muscleActivation):
    self.muscleActivation = muscleActivation
    
  def getNextActivation(self, theta):
    return 0 if theta < math.radians(90) else self.muscleActivation
    # return 0.4
  # taHealthyActivation = lambda theta: 12/5 * theta - 14/15 # testing linear function