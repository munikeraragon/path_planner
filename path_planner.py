''' This module server as an entry point of this path planning
    Framework. The module is in charge of fedding a map_object into
    the Loader, and then directing this to different path planning algorithims.'''

from visual.visual import Visual
from algorithms.dijkstra import Dijkstra


def main():
    map_file = 'C:/Users/santi/Desktop/Projects/path_planner/maps/mission_map.json'

    #dijkstra = Dijkstra(map_file)
    map_visual = Visual(map_file)


    map_visual.draw() # draw map visualization
    map_visual.simulate()

    ''' create Dijkstra object which will be transmitting points to the Visual object '''
    #map_visual.simulate(dijkstra.run)





if __name__ == '__main__':
    main()
