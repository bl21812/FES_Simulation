import math
from scipy import integrate

def simulate(f, initAngle, simTimeUpper, simTimeLower, muscles):
  '''
  f: function to pass into ivp solver
  initAngle: initial theta (rad) of the system
  simTimeUpper: upper bound on the simulation time
  simTimelower: lower bound on othe simulation time
  muscles: list of HillTypeMuscleModel objs used in the simulation 

  returns time, thetas, and the normal muscle length of the tibialis 
  ''' 
  # tolerances for simulation
  rtol = 10**-6
  atol = 10**-8

  # initial condition
  normalizedLengths = [0.6*muscle.muscleTendonLength(initAngle) for muscle in muscles]
  initialState = [initAngle, 0] + normalizedLengths
  
  output = integrate.solve_ivp( # uses RK45 by default
    fun = f,
    t_span = (simTimeLower, simTimeUpper),
    y0 = initialState,
    rtol = rtol,
    atol = atol,
    min_step = (simTimeUpper-simTimeLower)/100
  )

  time, y = output.t, output.y
  thetas = y[0]
  muscleNormLengths = y[2:]

  return time, thetas, muscleNormLengths