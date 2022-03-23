from helpers.Regression import modelEval

def forceVelocityMuscle(model, vm):
  '''
  @param model: Ridge regression model
  @param vm: muscle (contractile element) velocity) 
  
  returns force-velocity scale factor
  '''
 
  # train Ridge model then use model weights to predict vm
  return modelEval(vm, model.coef_, model.intercept_, 0.15)


