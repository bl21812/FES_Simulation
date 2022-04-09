from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

def plotOutput(time, thetas, torques, labels, colours, dir, fileName):
  if not os.path.exists(dir):
    os.mkdir(dir)
  
  thetas = np.degrees(thetas)
  df = pd.DataFrame({'time': time,
                    'theta': thetas,
                    'torque': torques[0]})
  df.to_csv(f"{dir}/{fileName}.csv")
  plt.rcParams.update({'font.size': 30})

  fig, axs = plt.subplots(2, figsize=(25, 25))
  axs[0].plot(time, thetas)
  axs[0].set(xlabel = "Time (s)", ylabel = "Theta (deg)")
  axs[0].grid(True)

  for i in range(len(torques)):
    axs[1].set(xlabel = "Time (s)", ylabel = "Torque (Nm)")
    axs[1].plot(time, torques[i], colours[i], label = labels[i])
    axs[1].legend(loc="upper right")
    axs[1].grid(True)
    
  plt.savefig(f"{dir}/{fileName}.png")
  print(f"Saving plot to {dir}/{fileName}.png")