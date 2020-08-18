"""

Path planning visualization module

author: Muniker Aragon

"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from .loader import Loader

class Visual():
  def __init__(self, file):
    self.map = Loader(file)

  def draw(self):
    # deserialize map
    boundary = self.map.boundary()
    waypoints = self.map.waypoints()
    obstacles = self.map.obstacles()

    # plot map features
    self.plot_obstacles(obstacles)
    self.plot_waypoints(waypoints)
    self.plot_boundary(boundary)

  def simulate(self):
    for i in range(0, 1000, 100):
      plt.plot(i,i, "xc")
      plt.pause(0.001)

    plt.show()

  ''' 
    The following methods should only be call inside this module
  ''' 
  
  def plot_obstacles(self, obstacles):
    x_coordinates, y_coordinates = self.project_coordinates(obstacles)
    radii = list(map(lambda point: point['radius']/3, obstacles))
    fig, ax = plt.subplots()

    for i in range(len(x_coordinates)):
        circle = plt.Circle((x_coordinates[i],y_coordinates[i]), radii[i])
        ax.set_aspect(1)
        ax.add_artist(circle)

  def plot_waypoints(self, waypoints):
    x_coordinates, y_coordinates = self.project_coordinates(waypoints)
    plt.plot(x_coordinates, y_coordinates)
    plt.grid(True)
    plt.axis("equal")

  def plot_boundary(self, boundary):
    xCoords, yCoords = self.project_coordinates(boundary)
    plt.plot(xCoords, yCoords)
    plt.grid(True)
    plt.axis("equal")


  def project_coordinates(self, coordinates):
    project = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    x_coordinates = []
    y_coordinates = []

    for point in coordinates:
        x_point,y_point = project(point['longitude'], point['latitude']) # project 
        x_coordinates.append(x_point - 8641750)
        y_coordinates.append(y_point - 3725600)

    return x_coordinates, y_coordinates
