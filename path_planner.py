''' This module serves as an entry point of this path planning
    Framework. The module is in charge connecting an Algorithim with 
    the visual module'''

from visual.visual import Visual
from algorithms.dijkstra import Dijkstra
from loader import Loader
import os


def main():
    # create a loader from map 
    map_file = os.getcwd() + '/maps/mission_map.json'
    loader = Loader(map_file, cartesian=False)
    
    #map_file = os.getcwd() + '/maps/test_map.json'
    #loader = Loader(map_file, cartesian=True)

    dijkstra = Dijkstra(loader)
    map_visual = Visual(loader)

    map_visual.draw() 
    map_visual.simulate(dijkstra) 


if __name__ == '__main__':
    main()
