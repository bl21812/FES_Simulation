class PID:
  '''
  Standard PID controller
  '''

  # Initialize P, I, and D constants and initial state
  def __init__(self, p, i, d, target, step, initState):
    '''
    @param p: 
    @param i: 
    @param d: 
    @param target: list of ideal normalized lengths (one per timestep)
    @param step: Float, size of one time step (seconds)
    '''
    self.Kp = p
    self.Ki = i
    self.Kd = d
    self.errors = []
    self.target = target
    self.state = initState
    self.timeStep = step

  def update(self, pred, k):
    '''
    @param pred: Float - predicted normalized length at timestep k
    @param k: Integer - timestep for which error is computed
    '''
    
    e = pred - self.target[k]
    lastErr = 0 if not self.errors else self.errors[-1]
    self.errors.append(e)
    
    p = self.Kp * e
    i = self.Ki * self.timeStep * sum(self.errors)
    d = self.Kd * (e - lastErr) / self.timeStep

    output = self.state + p + i + d
    self.state = output
    
    return output