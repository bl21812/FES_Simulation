import matplotlib.pyplot as plt

def plotOutput(time, thetas, torques, label, colour, fileName):
  fig, axs = plt.subplots(2, figsize=(25, 25))
  axs[0].plot(time, thetas)
  axs[0].set(xlabel = "Time (s)", ylabel = "Theta (rad)")
  axs[1].set(xlabel = "Time (s)", ylabel = "Torque (Nm)")
  axs[1].plot(time, torques, f'tab:{colour}', label = label)
  axs[1].legend(loc="upper right")
  axs[1].set_ylim([-25, 50])
  plt.savefig(f"images/{fileName}.png")