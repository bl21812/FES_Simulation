import matplotlib.pyplot as plt
import pandas as pd
import os

def plotOutput(time, thetas, torques, label, colour, fileName):
  dir = "scaled_images"
  if not os.path.exists(dir):
    os.mkdir(dir)
  
  df = pd.DataFrame({'time': time,
                    'theta': thetas,
                    'torque': torques})
  df.to_csv(f"{dir}/{fileName}.csv")

  fig, axs = plt.subplots(2, figsize=(25, 25))
  axs[0].plot(time, thetas)
  axs[0].set(xlabel = "Time (s)", ylabel = "Theta (rad)")
  axs[1].set(xlabel = "Time (s)", ylabel = "Torque (Nm)")
  axs[1].plot(time, torques, f'tab:{colour}', label = label)
  axs[1].legend(loc="upper right")
  # axs[1].set_ylim([-1, 1])
  plt.savefig(f"{dir}/{fileName}.png")
  print(f"Saving plot to {dir}/{fileName}.png")