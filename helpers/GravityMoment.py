import math

def gravityMoment(theta, mass):
  ankleMass = 0.0133 * mass
  g = 9.81
  dComAnkle = 0.05

  # if theta > math.pi/2:
  #   return dComAnkle * ankleMass * g * math.sin(theta - math.pi/2)
  # else:
  #   return dComAnkle * ankleMass * g * math.cos(theta - math.pi/2)
  # return dComAnkle * ankleMass * g * math.cos(theta - math.pi/2)
  return dComAnkle * ankleMass * g * math.sin(math.pi/2-theta)