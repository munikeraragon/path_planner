'''
  This module deserializer map_objects.
  The Loader assumes that the input will contain
  polar coordinates in json format. 
'''

from mpl_toolkits.basemap import Basemap
import numpy as np
import json


class Loader:

    def __init__(self, file_path, cartesian=False):
        self.map_object = json.loads(open(file_path).read())
        self.cartesian = cartesian


    def boundary(self):
        fly_zone = self.map_object['flyZones'][0]
        boundary = fly_zone['boundaryPoints']

        if self.cartesian:
            x_coordinates, y_coordinates = self.get_coordinates(boundary)
        else:
            x_coordinates, y_coordinates = self.project_coordinates(boundary)

        return x_coordinates, y_coordinates


    def waypoints(self):
        waypoints = self.map_object['waypoints']

        if self.cartesian:
            x_coordinates, y_coordinates = self.get_coordinates(waypoints)

        else: 
            x_coordinates, y_coordinates = self.project_coordinates(waypoints)

        return x_coordinates, y_coordinates


    def obstacles(self):
        obstacles = self.map_object['stationaryObstacles']
        radii = list(map(lambda point: point['radius']/3, obstacles))

        if self.cartesian:
            x_coordinates, y_coordinates = self.get_coordinates(obstacles)

        else:
            x_coordinates, y_coordinates = self.project_coordinates(obstacles)

        return x_coordinates, y_coordinates, radii



    def project_coordinates(self, coordinates):
        project = Basemap(width=12000000,height=9000000,projection='lcc',
                            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
        x_coordinates = []
        y_coordinates = []

        for point in coordinates:
            x_point,y_point = project(point['longitude'], point['latitude'])
            x_coordinates.append(x_point - 8641750)
            y_coordinates.append(y_point - 3725600)

        # add coordinate[0] to close polygon when drawing
        x_point,y_point = project(coordinates[0]['longitude'], coordinates[0]['latitude'])
        x_coordinates.append(x_point - 8641750)
        y_coordinates.append(y_point - 3725600)

        return x_coordinates, y_coordinates



    def get_coordinates(self, coordinates):
        x_coordinates = []
        y_coordinates = []

        for point in coordinates:
            x_coordinates.append(point['x'])
            y_coordinates.append(point['y'])

        # add coordinate[0] to close polygon when drawing
        x_coordinates.append(coordinates[0]['x'])
        y_coordinates.append(coordinates[0]['y'])
        return x_coordinates, y_coordinates


    