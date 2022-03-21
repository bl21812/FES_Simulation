from helpers.MuscleVelocity import getMuscleVelocity
from helpers.constants import ankleInertia

# Wrapper for the system of state-space equations.
def model(x, muscles):
  '''
  @param: x: state vector [ankle angle, angular velocity, muscle normalized CE lengths...]
  @param muscles: list of HillTypeMuscleModel objs. the order corresponds to the muscle normalized CE lengths from x at index 2 onwards
  '''
  theta, angularVelocity = x[:2]
  normMuscleLengths = x[2:]

  assert len(muscles) == len(normMuscleLengths)

  muscleNormLengthDerivs = [] 
  muscleTorques = []
  for muscle, normMuscleLength in zip(muscles, normMuscleLengths):
    # first find the params to find the length derivatives
    muscleTendonLength = muscle.muscleTendonLength(theta)
    normTendonLength = muscle.normTendonLength(muscleTendonLength, normMuscleLength)
    lengthDeriv = getMuscleVelocity(muscle.activationFunc(), normMuscleLength, normTendonLength)
    muscleNormLengthDerivs.append(lengthDeriv)

    # also calculate the torques generated by each muscle
    torque = muscle.momentArm * muscle.getForce(muscleTendonLength, normMuscleLength)
    muscleTorques.append(torque)

  # since we are only consisdering the anterior muscles, the torques should be multiplied by -1
  # we will also assume there is no external force. 
  angularVelocityDeriv = ankleTorque(theta)/ankleInertia
  
  return [angularVelocity, angularVelocityDeriv] + muscleNormLengthDerivs


def ankleTorque(theta):
  '''
  @param theta: angle of the ankle 
  
  Returns the approximated ankle torque given the ankle angle. 
  Function is a fourth order polynomial, which approximates the ankle torque based on data from toe off to maximum flexion point of the ankle during swing phase.
  '''
  a = 0.9020654093720372
  b = 0.08667091369408163
  c = 0.0006433455433876395
  d = -0.0001440269888009832
  e = -0.000003875116084345257

  return a + (b * theta) + (c * theta**2) + (d * theta**3) + (e * theta**4)
  