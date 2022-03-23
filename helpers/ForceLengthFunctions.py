def forceLengthTendon(lt):
  ''' 
  Determine force produced by series elastic element

  @param lt: normalized length of series elastic elements
  '''     
  return 10 * (lt-1) + 240 * (lt-1)**2 if lt >= 1 else 0

def forceLengthParallel(lm):
  ''' 
  Determine normalized force produced by contractile element

  @param lm: normalized length of contractile elements
  ''' 
  return (3 * (lm - 1)**2)/(0.6 + lm - 1) if lm >= 1 else 0


def forceLengthMuscle(model, normMuscleLength):
  '''
  Determine force-length scale factors
  
  @param model: Gaussian model
  @param normMuscleLength: normalized length of contractile elements
  '''
  return model.predict([[normMuscleLength]])[0]


