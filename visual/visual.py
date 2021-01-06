"""

Path planning visualization module

author: Muniker Aragon

"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

class Visual():
  def __init__(self, loader):
    self.map = loader

  def draw(self):
    # plot map features
    self.plot_obstacles()
    self.plot_way_points()
    self.plot_boundary()

  def simulate(self, algorithm):
    plt.grid(True)
    final_path = algorithm.run(plt)
    plt.show()


  ''' 
        The following methods should only be call inside this module
  ''' 

  def plot_boundary(self):
    x_coords, y_coords = self.map.boundary()
    plt.plot(x_coords, y_coords)
    plt.grid(True)
    plt.axis("equal")
    
  def plot_way_points(self):
    x_coords, y_coords =  self.map.way_points()
    plt.plot(x_coords, y_coords)
    plt.grid(True)
    plt.axis("equal")

  def plot_obstacles(self):
    x_coords, y_coords, radii = self.map.obstacles()
    fig, ax = plt.subplots()
    for i in range(len(radii)):
        circle = plt.Circle((x_coords[i],y_coords[i]), radii[i])
        ax.set_aspect(1)
        ax.add_artist(circle)