import numpy as np
import math

def find_d(cFunc):
    derivCFunc = lambda d : -1 * a * math.exp(a / d) / (b * (d ** 2))
    return 

class FES:

  def __init__(self, n1Func):
    self.neuralActivations = []
    A = 0.05
    a10 = 0.3085 + A * np.sin(math.pi/4)
    u0 = 0.3085 - A * np.cos(math.pi/4)
    m = (1 - a10) / (1 - u0)
    b = (a10 - u0) / (1 - u0)

    cFunc = lambda d : (math.exp(a10 / d) - 1) / u0

    d = find_d(cFunc)
    c = cFunc(d)

    self.alpha = 0.9486
    self.beta1 = -0.056
    self.beta2 = 0.000627
    
    self.activation_low = lambda u : d * math.log(c * u + 1)
    self.activation_high = lambda u : m * u + b

    self.u0 = u0

  def genEMG(self, type, params, freq):
    '''
    Generate sEMG for calling FES instance based on given params

    @param type: String, type of sEMG signal ('sin', 'cos', or 'const')
    @param params: Dictionary of sEMG signal parameters
      For sinusoids, keys a and b, where N1(t) = asint + b or acost + b
      For constant, key a, where N1(t) = a
    @param freq: Float, frequency (Hz) at which sEMG is sampled
    '''

    self.currTimestep = 0
    self.times = np.linspace(0, 5, 5 * freq + 1) # timestamps, s
    self.emg = None
    
    if type == 'const':
      assert('a' in params and 'b' in params)
      self.emg = lambda t : params['a']
    else:
      assert ('a' in params)
      if type == 'sin':
        self.emg = lambda t : params['a'] * math.sin(t) + params['b']
      elif type == 'cos':
        self.emg = lambda t : params['a'] * math.cos(t) + params['b']
      else:
        raise ValueError('Accepted types are sin, cos and const')

  def getNextActivation(self):
    
    t = self.times[self.currTimestep]

    uMinus1 = 0 if not self.neuralActivations else self.neuralActivations[-1]
    uMinus2 = 0 if len(self.neuralActivations) < 2 else self.neuralActivations[-2]

    u = self.alpha * self.emg(t) - (self.beta1 * uMinus1) - (self.beta2 * uMinus2)

    # APPEND TO NEURAL ACTIVATIONS LIST
    self.currTimestep += 1
    
    return