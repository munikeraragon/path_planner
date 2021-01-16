from mpl_toolkits.basemap import Basemap
import numpy as np
import json


class Loader:
    def __init__(self, file_path, cartesian=False):
        self.map = json.loads(open(file_path).read())
        self.cartesian = cartesian


    def start_point(self):
        '''
            Extract starting coordinates from a map file.
        '''
        starting_coord = self.map['startPoint']
        project = Basemap(width=12000000,height=9000000,projection='lcc',
                            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

        if self.cartesian:
            x_coord, y_coord = starting_coord['x'], starting_coord['y']

        else:
            x_coord, y_coord= project(starting_coord['longitude'], starting_coord['latitude'])
            x_coord += -8641750
            y_coord += -3725600

        return x_coord, y_coord


    def target_point(self):
        '''
            Extract target coordinates from a map file.
        '''
        target_coord = self.map['targetPoint']
        project = Basemap(width=12000000,height=9000000,projection='lcc',
                            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

        if self.cartesian:
            x_coord, y_coord = target_point['x'], target_point['y']

        else:
            x_coord, y_coord= project(target_point['longitude'], target_point['latitude'])
            x_coord += -8641750
            y_coord += -3725600

        return x_coord, y_coord


    def boundary(self):
        '''
            Extract boundary coordinates from a map file.
        '''
        fly_zone = self.map['flyZones'][0]
        boundary = fly_zone['boundaryPoints']

        if self.cartesian:
            x_coords, y_coords = self.get_coordinates(boundary)
        else:
            x_coords, y_coords = self.project_coordinates(boundary)

        return x_coords, y_coords


    def way_points(self):
        '''
            Extract boundary waypoints coordinates from a map file.
        '''
        way_points = self.map['waypoints']

        if self.cartesian:
            x_coords, y_coords = self.get_coordinates(way_points)

        else: 
            x_coords, y_coords = self.project_coordinates(way_points)

        return x_coords, y_coords


    def obstacles(self):
        '''
            Extract boundary waypoints obstacle coordinates from a map file.
        '''
        obstacles = self.map['stationaryObstacles']
        radii = list(map(lambda point: point['radius']/3, obstacles))

        if self.cartesian:
            x_coords, y_coords = self.get_coordinates(obstacles)

        else:
            x_coords, y_coords = self.project_coordinates(obstacles)

        return x_coords, y_coords, radii



    def project_coordinates(self, coordinates):
        '''
            This method projects polar coordinates into cartesian.
        '''
        project = Basemap(width=12000000,height=9000000,projection='lcc',
                            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
        x_coords = []
        y_coords = []

        for point in coordinates:
            x_point,y_point = project(point['longitude'], point['latitude'])
            x_coords += [x_point - 8641750]
            y_coords += [y_point - 3725600]

        # close polygon drawing by adding coordinate[0]
        x_point,y_point = project(coordinates[0]['longitude'], coordinates[0]['latitude'])
        x_coords += [x_point - 8641750]
        y_coords += [y_point - 3725600]

        return x_coords, y_coords



    def get_coordinates(self, coordinates):
        '''
            This method separates a cordinate dictionary into an x and y array.
        '''
        x_coords = []
        y_coords = []

        for point in coordinates:
            x_coords += [point['x']]
            y_coords += [point['y']]

        # close polygon drawing by adding coordinate[0]
        x_coords += [coordinates[0]['x']]
        y_coords += [coordinates[0]['y']]
        return x_coords, y_coords


    