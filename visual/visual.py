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
    self.plot_waypoints()
    self.plot_boundary()
    #plt.show()

  def simulate(self, algorithm):
    plt.grid(True)
    algorithm.run(plt)
    plt.show()


  ''' 
        The following methods should only be call inside this module
  ''' 

  def plot_boundary(self):
    xCoords, yCoords = self.map.boundary()
    plt.plot(xCoords, yCoords)
    plt.grid(True)
    plt.axis("equal")
    
  def plot_waypoints(self):
    x_coordinates, y_coordinates =  self.map.waypoints()
    plt.plot(x_coordinates, y_coordinates)
    plt.grid(True)
    plt.axis("equal")

  def plot_obstacles(self):
    x_coordinates, y_coordinates, radii = self.map.obstacles()
    fig, ax = plt.subplots()
    for i in range(len(radii)):
        circle = plt.Circle((x_coordinates[i],y_coordinates[i]), radii[i])
        ax.set_aspect(1)
        ax.add_artist(circle)