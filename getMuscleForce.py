import numpy as np
import sklearn

def getMuscleForceLengthRegression() -> list:
# TASK 2

# Input Parameters
# data(:,1): samples of an independent variable
# data(:,2): corresponding samples of a dependent variable

# Output
# force_length_regression: the genered Gaussian model

  length = data(:,1)
  force = data(:,2)

# Define data points

# Normalization
  scaledForce = rescale(force)
  [~, idx] = max(force)

# Regression with "fit" function with "gauss2" option as model type
  forceLengthRegression = fit(normalizedLengh,scaledForce, 'gauss2')

  return

def getMuscleForceVelocityRegression() -> list:
# 1D regression model with Gaussian basis functions.

# Input Parameters
# data(:,1): samples of an independent variable
# data(:,2): corresponding samples of a dependent variable

data = [-1.0028395556708567, 0.0024834319945283845
    -0.8858611825192801, 0.03218792009622429
    -0.5176245843258415, 0.15771090304473967
    -0.5232565269687035, 0.16930496922242444
    -0.29749770052593094, 0.2899790099290114
    -0.2828848376217543, 0.3545364496120378
    -0.1801231103040022, 0.3892195938775034
    -0.08494610976156225, 0.5927831890757294
    -0.10185137142991896, 0.6259097662790973
    -0.0326643239546236, 0.7682365981934388
    -0.020787245583830716, 0.8526638522676352
    0.0028442725407418212, 0.9999952831301149
    0.014617579774061973, 1.0662107025777694
    0.04058866536166583, 1.124136223202283
    0.026390887007381902, 1.132426122025424
    0.021070257776939272, 1.1986556920827338
    0.05844673474682183, 1.2582274002971627
    0.09900238201929201, 1.3757434966156459
    0.1020023112662436, 1.4022310794556732
    0.10055894908138963, 1.1489210160137733
    0.1946227683309354, 1.1571212943090965
    0.3313459588217258, 1.152041225442796
    0.5510200231126625, 1.204839508502158];

  velocity = data(:,1);
  force = data(:,2);

# Ridge Regression
# NOTE: this is different than TASK 2 of Question 1, follow the instruction
# for TASK 2
fun = @(x, mu, sigma) 1./(1+exp(-(x-mu)./sigma));
X = [];
for i = -1:0.2:-0.1
    X = [X fun(velocity, i, 0.15)];
end
force_velocity_regression = ridge(force, X, 1, 0);
end