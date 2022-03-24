from helpers.ForceLengthFunctions import forceLengthTendon
import numpy as np
import math

class HillTypeMuscleModel:
  '''
  Damped Hill-type muscle model adapted from Millard et al. (2013).The dynamic model is defined in terms of normalized length and velocity.To model a particular muscle, scale factors are needed for force, CE length, and SE length.
  '''
  def __init__(self, f0m, theta, insertion, origin, momentArm, activationModel, pennation):
    '''
    @param f0m: maximum isometric force (N)
    @param theta: the starting position of the muscle
    @param insertion: coordinates of muscle insertion
    @param origin: coordinates of muscle origin
    @param momentArm: length of the moment arm for the muscle.
    @param activationModel: a model of type 'activation'. used for invoking the next activation
    @parma pennation: pennation angle of the muscle
    '''
    self.f0m = f0m 
    self.insertion = insertion
    self.origin = origin
    self.momentArm = momentArm
    self.activationModel = activationModel
    self.pennation = pennation
    
    muscleTendonLength = self.muscleTendonLength(theta)
    self.restingMuscleLength = 0.6 * muscleTendonLength # actual length (m) of muscle (CE) that corresponds to normalized length of 1
    self.restingTendonLength = 0.4 * muscleTendonLength # actual length of tendon (m) that corresponds to normalized length of 1 

  def normTendonLength(self, muscleTendonLength, normMuscleLength) -> int:
    ''' 
    Determine the noramlized length of the tendon
    
    @param muscleTendonLength: non-normalized length of the full muscle-tendon complex (m)
    @param normMuscleLength: normalized length of the contractile element (state varaible)
    @param restingMuscleLength: actual length (m) of muscle (CE) that corresponds to normalized length of 1
    '''
    return (muscleTendonLength - self.restingMuscleLength * normMuscleLength) / self.restingTendonLength

  def getForce(self, muscleTendonLength, normMuscleLength):
    ''' 
    Determine the muscle tension 

    @param muscleTendonLength: non-normalized length of the full muscle-tendon complex (m)
    @param normMuscleLength: normalized length of the contractile element (state varaible)
    '''
    normTendonLength = self.normTendonLength(muscleTendonLength, normMuscleLength)
    return self.f0m * forceLengthTendon(normTendonLength)


  def muscleTendonLength(self, theta):
    '''
    Calculates the muscle tendon length (total length)

    @param theta: body angle (up from prone horizontal)
    '''
    # define rotation matrix
    rotation = np.matrix([[math.cos(theta), -1 * math.sin(theta)], 
                          [math.sin(theta), math.cos(theta)]])

    # coordinates in global reference frame
    globalOrigin = np.matmul(rotation, np.transpose(self.origin)) # 1x2 matrix
    difference = globalOrigin - self.insertion; # 1x2 matrix
    
    muscleTendonLength = math.sqrt(difference[0,0]**2 + difference[0,1]**2)
    return muscleTendonLength