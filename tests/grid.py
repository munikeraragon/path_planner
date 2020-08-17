'''
  This script creates a simple grid and starts coloring
  some of the cells '''


import matplotlib.pyplot as plt
import matplotlib
import numpy as np 

# Controller
class Grid:
  def __init__(self, row, col):
    self.grid = np.empty(shape=(row, col))
    self.grid.fill(np.nan)

    # make a figure + axes
    self.fig, self.ax = plt.subplots(1, 1, tight_layout=True)

    # make color map
    self.my_cmap = matplotlib.colors.ListedColormap(['r', 'g', 'b'])
    self.my_cmap.set_bad(color='w', alpha=0)

  def visualize(self):
    # draw the grid
    for x in range(4):
      self.ax.axhline(x, lw=2, color='k', zorder=5)
      self.ax.axvline(x, lw=2, color='k', zorder=5)
    self.ax.imshow(self.grid , interpolation='none', cmap=self.my_cmap, extent=[0, 4, 0, 4], zorder=0)
    plt.draw()
    plt.pause(2)
  
  def fill(self, row, col):
    self.grid[row, col] = 1




def main():
  grid = Grid(4,4)
  grid.visualize()
  grid.fill(0,0)
  grid.visualize()
  grid.fill(0,1)
  grid.visualize()



main()

