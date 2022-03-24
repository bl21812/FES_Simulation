import math
from scipy import integrate

def simulate(f, tibialis, simTimeUpper, simTimeLower):   
  # tolerances for simulation
  rtol = 10**-6
  atol = 10**-8

  # initial condition
  initialState = [math.radians(110), 0, 1]
  
  output = integrate.solve_ivp( # uses RK45 by default
    fun = f,
    t_span = (simTimeLower, simTimeUpper),
    y0 = initialState,
    rtol = rtol,
    atol = atol
  )

  time, y = output.t, output.y
  thetas, _, taMuscleNormLengths = y

  return time, thetas, taMuscleNormLengths