import numpy as np
from activations.fes import FES

def nearest_index(arr, t):
  '''
  @param arr: array [times, thetas]
  @param t: time point that we want to find the nearest time to 
  '''
  return (np.abs(np.array(arr[0]) - t)).argmin()

class PID(FES):
  '''
  Standard PID controller
  '''
  def __init__(self, p, i, d, target, initState):
    '''
    @param p: Constant
    @param i: Constant
    @param d: Constant
    @param target: Size 2 list, target[0] is times, target[1] is thetas
    @param initState: Initial theta
    '''
    self.Kp = p
    self.Ki = i
    self.Kd = d
    self.errors = []
    self.target = target
    self.state = initState
    self.times = []

    super().__init__()

  def getNextActivation(self, theta, t):
    '''
    @param theta: theta at given timestep
    @param t: time for given timestep

    returns: the next activation
    '''
    emg = self.update(theta, t)
    return self.getActivationFromEmg(emg)

  def getActivationFromEmg(self, emg):
    '''
    @param emg: value of an emg signal at a given time step
    returns the activation for the given value of the emg signal 
    '''
    uMinus1 = 0 if not self.neuralActivations else self.neuralActivations[-1]
    uMinus2 = 0 if len(self.neuralActivations) < 2 else self.neuralActivations[-2]

    u = self.alpha * emg - (self.beta1 * uMinus1) - (self.beta2 * uMinus2)

    act = self.activation_low(u) if u < self.u0 and u >= 0 else self.activation_high(u)

    self.neuralActivations.append(u)
    
    return act

  def update(self, pred, t):
    '''
    @param pred: Float - predicted theta at timestep k
    @param t: current timestep 
    '''
    
    pred_ind = nearest_index(self.target, t)

    e = pred - self.target[1][pred_ind]
    lastErr = 0 if not self.errors else self.errors[-1]
    lastTime = 0 if not self.times else self.times[-1]

    self.errors.append(e)
    self.times.append(t)
    
    p = self.Kp * e
    i = self.Ki * self.error_integral()
    deltaT = t - lastTime
    d = 0 if deltaT == 0 else self.Kd * (e - lastErr) / deltaT

    output = self.state + p + i + d
    self.state = output

    return output

  def error_integral(self):
    if len(self.errors) < 2:
      return 0
    error_int = 0
    for i in range(len(self.errors)-1):
      error_int += self.errors[i] * (self.times[i+1] - self.times[i])
    return error_int