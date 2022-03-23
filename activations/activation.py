import abc

class activation:
  @abc.abstractmethod
  def getNextActivation(self, theta = 0):
    pass 