''' This module server as an entry point of this path planning
    Framework. The module is in charge connecting an Algorithim with 
    the visual module'''

from visual.visual import Visual
from algorithms.dijkstra import Dijkstra
from loader import Loader
import os


def main():
    # create a loader from map 
    map_file = os.getcwd() + '/maps/mission_map.json'
    loader = Loader(map_file)

    # both the visual module and the algorithim
    # will use the loader
    dijkstra = Dijkstra(loader)
    map_visual = Visual(loader)

    #map_visual.draw()  # draw map visualization

    # pass an algorithim to visual module
    # and run the simulation
    map_visual.simulate(dijkstra) 


if __name__ == '__main__':
    main()
