''' This module serves as an entry point of this path planning Framework.
    The module is in charge connecting an Algorithim with the visual module '''

from visual.visual import Visual
from loader import Loader
import sys
import os

from algorithms.dijkstra.multithread import Dijkstra as DijkstraASync
from algorithms.dijkstra.singlethread import Dijkstra as DijkstraSync
from algorithms.astar.multithread import Astar as AstarAsync
from algorithms.astar.singlethread import Astar as AstarSync
from algorithms.rrt import RRT

def main(algo, thread):
    # load map
    map_file = os.getcwd() + '/maps/mission_map.json'
    loader = Loader(map_file, cartesian=False)

    #map_file = os.getcwd() + '/maps/test_map.json'
    #loader = Loader(map_file, cartesian=True)
    

    # choose algorithm

    if algo == 'dijkstra':
        if thread == 'single':
            algo = DijkstraSync(loader)
        if thread == 'multi':
            algo = DijkstraASync(loader)

    if algo == 'astar':
        if thread == 'single':
            algo = AstarSync(loader)
        if thread == 'multi':
            algo = AstarAsync(loader)

    if algo == 'rrt':
        algo =  RRT(loader) 

    
    visual = Visual(loader)
    visual.draw() 
    visual.simulate(algo)





if __name__ == '__main__':
    argc = len(sys.argv)    
    if (argc > 2):
        main(algo=sys.argv[1], thread=sys.argv[2])
    elif (argc > 1):
        main(algo=sys.argv[1], thread='single')
    else:
        main(algo='astar', thread='single')



