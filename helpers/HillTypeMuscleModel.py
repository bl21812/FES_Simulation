from ForceLengthFunctions import forceLengthTendon
import numpy as np
import math

class HillTypeMuscleModel:
  '''
  Damped Hill-type muscle model adapted from Millard et al.   (2013).The dynamic model is defined in terms of     normalized length and velocity.To model a particular   muscle, scale factors are needed for force, CE length, and SE length.
  '''
  def __init__(self, f0m, restingMuscleLength, restingTendonLength, insertion, origin):
    '''
    @param f0m: maximum isometric force (N)
    @param restingMuscleLength: actual length (m) of muscle (CE) that corresponds to normalized length of 1
    @param restingTendonLength: actual length of tendon (m) that corresponds to normalized length of 1 
    @param insertion: coordinates of muscle insertion
    @param origin: coordinates of muscle origin
    '''
    self.f0m = f0m 
    self.restingMuscleLength = restingMuscleLength
    self.restingTendonLength = restingTendonLength
    self.insertion = insertion
    self.origin = origin

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
    rotation = np.matrix([[math.cos(theta), math.sin(theta)], 
                          [math.sin(theta), math.cos(theta)]])
    
    # coordinates in global reference frame
    globalOrigin = np.dot(rotation, self.origin)
    
    difference = globalOrigin - self.insertion;
    muscle_tendon_length = math.sqrt(difference[0]**2 + difference[1]**2)
    return muscle_tendon_length