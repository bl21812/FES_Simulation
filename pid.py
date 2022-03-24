import numpy as np

def nearest_index(arr, t):
  # arr[0] is list of times
  return (np.abs(arr[0] - t)).argmin()

class PID:
  '''
  Standard PID controller
  '''

  # Initialize P, I, and D constants and initial state
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

  def update(self, pred, t):
    '''
    @param pred: Float - predicted theta at timestep k
    @param t: Time
    '''
    
    pred_ind = nearest_index(self.target, t)

    e = pred - self.target[pred_ind]
    lastErr = 0 if not self.errors else self.errors[-1]
    lastTime = 0 if not self.times else self.times[-1]

    self.errors.append(e)
    self.times.append(t)
    
    p = self.Kp * e
    i = self.Ki * self.error_integral()
    d = self.Kd * (e - lastErr) / (t - lastTime)

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