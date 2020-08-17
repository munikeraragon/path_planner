'''
  This module server as a deserializes map loader.
  This loader assumes that input map_objects will contain
  polar coordintes and that they will be in json format. 
''' 
import json

class Loader():
  def __init__(self, file_path):
    self.map_object = json.loads(open(file_path).read())

  def waypoints(self):
    waypoints = self.map_object['waypoints']
    return waypoints

  def obstacles(self):
    obstacles = self.map_object['stationaryObstacles']
    return obstacles

  def boundary(self):
    fly_zone = self.map_object['flyZones'][0]
    boundary = fly_zone['boundaryPoints']
    return boundary


