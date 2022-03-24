import abc

class activation:
  '''
  Abstract class representing the different activation models.
  '''
  @abc.abstractmethod
  def getNextActivation(self, theta = 0, t = 0):
    pass 