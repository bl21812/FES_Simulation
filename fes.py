import numpy as np
import math
from scipy import optimize

class FES:

  def __init__(self):
    self.neuralActivations = []
    self.A = 0.05
    self.a10 = 0.3085 + self.A * np.sin(math.pi/4)
    self.u0 = 0.3085 - self.A * np.cos(math.pi/4)
    self.m = (1 - self.a10) / (1 - self.u0)
    self.b = (self.a10 - self.u0) / (1 - self.u0)

    cFunc = lambda d : (math.exp(self.a10 / d) - 1) / self.u0
    self.d = self.find_d(cFunc)
    self.c = cFunc(self.d)

    self.alpha = 0.9486
    self.beta1 = -0.056
    self.beta2 = 0.000627
    
    self.activation_low = lambda u : self.d * math.log(self.c * u + 1)
    self.activation_high = lambda u : self.m * u + self.b

  def find_d(self, cFunc):
    # use Newton-Raphson method to find d 
    f = lambda d: self.m - d * cFunc(d) / (cFunc(d) * self.u0 + 1)
    fPrime = lambda d: (1 / self.u0) * (-1 + (1 - self.a10 / d) * math.exp(-1 * self.a10 / d))
    d = optimize.newton(f, self.u0, fprime = fPrime, tol = 10**-5)
    return d

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
      assert ('a' in params)
      self.emg = lambda t : params['a']
    else:
      assert('a' in params and 'b' in params)
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