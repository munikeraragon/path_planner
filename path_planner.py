''' This module server as an entry point of this path planning
    Framework. The module is in charge connecting an Algorithim with 
    the visual module'''

from visual.visual import Visual
from algorithms.dijkstra import Dijkstra
from loader import Loader


def main():
    map_file = 'C:/Users/santi/Desktop/Projects/path_planner/maps/mission_map.json'
    loader = Loader(map_file)

    dijkstra = Dijkstra(loader)
    map_visual = Visual(loader)

    #map_visual.draw()  # draw map visualization
    map_visual.simulate(dijkstra)  # visual will simulate a passed algorithim


if __name__ == '__main__':
    main()
