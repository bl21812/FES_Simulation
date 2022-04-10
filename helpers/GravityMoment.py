import math

def gravityMoment(theta, mass):
  ankleMass = 0.0133 * mass
  g = 9.81
  dComAnkle = 0.05

  return dComAnkle * ankleMass * g * math.sin(math.pi/2-theta)