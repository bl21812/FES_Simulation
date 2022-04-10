import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

def plotOutput(time, thetas, torques, labels, colours, dir, fileName, muscleNormLengths = None, fes = None):
  '''
  @param time: list of time points
  @param thetas: list of theta points
  @param torques: list of lists of torques. ex. [[torque1], [torque2]...] corresponding to diff muscles
  @param labels: labels corresponding to the muscles the torques represent
  @param dir: file directory
  @param fileName: file name
  @param muscleNormLengths: list of list of normal muscle lengths. ex. [[norm1], [norm2]...]
  @param fes: function for the fes signal.

  Note that only one of normal muscle lengths and the FES can be plotted
  '''
  if not os.path.exists(dir):
    os.mkdir(dir)
  
  thetas = np.degrees(thetas)
  df = pd.DataFrame({'time': time,
                    'theta': thetas,
                    'torque': torques[0]})
  df.to_csv(f"{dir}/{fileName}.csv")
  plt.rcParams.update({'font.size': 30})

  plotMuscleNormLengths = muscleNormLengths is not None
  plotFes = fes is not None

  _, axs = plt.subplots(2, figsize=(25, 25)) if not plotMuscleNormLengths and not plotFes else plt.subplots(3, figsize=(25, 25))
  axs[0].plot(time, thetas)
  axs[0].set(xlabel = "Time (s)", ylabel = "Theta (deg)")
  axs[0].grid(True)

  for i in range(len(torques)):
    axs[1].set(xlabel = "Time (s)", ylabel = "Torque (Nm)")
    axs[1].plot(time, torques[i], colours[i], label = labels[i])
    axs[1].legend()
    axs[1].grid(True)

  if plotMuscleNormLengths:
    for i in range(len(muscleNormLengths)):
      axs[2].set(xlabel = "Time (s)", ylabel = "Normalized Muscle Length")
      axs[2].plot(time, muscleNormLengths[i], colours[i], label = labels[i])
      axs[2].legend()
      axs[2].grid(True)
  elif plotFes:
    fesOutput = np.array([fes(t) for t in time])
    fesOutput = fesOutput * 1000
    axs[2].set(xlabel = "Time (s)", ylabel = "FES Signal(mV)")
    axs[2].plot(time, fesOutput)
    axs[2].grid(True)
    
  plt.savefig(f"{dir}/{fileName}.png")
  print(f"Saving plot to {dir}/{fileName}.png")