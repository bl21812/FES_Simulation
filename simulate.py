import math
from scipy import integrate

def simulate(f, initAngle, simTimeUpper, simTimeLower):
  '''
  f: function to pass into ivp solver
  initAngle: initial theta (degrees) of the system
  simTimeUpper: upper bound on the simulation time
  simTimelower: lower bound on othe simulation time

  returns time, thetas, and the normal muscle length of the tibialis 
  ''' 
  # tolerances for simulation
  rtol = 10**-6
  atol = 10**-8

  # initial condition
  initialState = [math.radians(initAngle), 0, 1]
  
  output = integrate.solve_ivp( # uses RK45 by default
    fun = f,
    t_span = (simTimeLower, simTimeUpper),
    y0 = initialState,
    rtol = rtol,
    atol = atol
  )

  time, y = output.t, output.y
  thetas = y[0]
  muscleNormLengths = y[2:]

  return time, thetas, muscleNormLengths