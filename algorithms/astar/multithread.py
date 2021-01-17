from matplotlib.path import Path
import numpy as np
import math

import threading
import time


class Astar:
    def __init__(self, loader):
        self.map = loader
        self.base = 10

        self.motion = self.get_motion_model()
        self.boundary = self.boundary_path()
        self.obstacles = self.obstacle_path()


    class Node:
        def __init__(self, x, y, cost, parent_key):
            self.x = x
            self.y = y
            self.cost = cost
            self.parent_key = parent_key
        
    
        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.parent_key)


    def run(self, dinamic_plot=False):
        '''
            Initiate algorithim by breaking the waypoints
            into segmets and running Astart asyncroniously.

        '''

        x_coords, y_coords = self.map.way_points()
        way_points = np.array(list(zip(x_coords, y_coords)))

        x_start, y_start = way_points[0][0], way_points[0][1]
        x_start, y_start = self.base_rounding(x_start, y_start, self.base)


        threads = []
        segment_path = [list() for i in range(len(way_points))]

        for i, point in enumerate(way_points):
            x_target, y_target = self.base_rounding(point[0], point[1], self.base)

            try:
                x = threading.Thread(target=self.run_segment, args=(x_start, y_start, x_target, y_target, segment_path[i]))
                threads += [x]
                x.start()
            except Exception as e:
                print ("Error: unable to start thread")
                print(e)
        
            
            # updates starting postion to be used in the next segment
            x_start = x_target
            y_start = y_target
        

        for i, thread in enumerate(threads):
            thread.join() 

        print('Main thread exited')
        return segment_path




    
    def run_segment(self, x_start, y_start, x_target, y_target, segment_path):
        '''
            Execute Astar algorithim starting from
            (x_start, y_start) to (x_target, y_target). 
        '''

        visited_nodes = dict()
        priority_queue = dict()


        start_node = self.Node(x_start, y_start, 0, None) 
        start_key = str(x_start) + str(y_start)


        priority_queue[start_key] = start_node

        while len(priority_queue) != 0:
            current_node = self.lowest_cost_node(x_target, y_target, priority_queue)

            self.inspect_neighbords(current_node, priority_queue, visited_nodes)

            # check if destination has been reached
            if current_node.x == x_target and current_node.y == y_target:
                l = self.create_segment_path(current_node, visited_nodes)
                l.reverse()
                segment_path += l
                break

        

    def inspect_neighbords(self, node, priority_queue, visited_nodes):
        parent_key = str(node.x) + str(node.y)

        # create neighbords using the motion model
        for move_x, move_y, move_cost in self.motion:
            neighbord = self.Node(node.x+move_x, node.y+move_y, node.cost+move_cost, parent_key)

            if self.valid_node(neighbord):
                key = str(neighbord.x) + str(neighbord.y)

                if key in priority_queue:
                    if neighbord.cost < priority_queue[key].cost:
                        priority_queue[key] = neighbord
                

                if key not in visited_nodes and key not in priority_queue:
                    priority_queue[key] = neighbord  

        visited_nodes[parent_key] = node


    def target_distance(self, x_target, y_target, x, y):
        return math.sqrt(pow(x_target-x,2) + pow(y_target-y, 2))


    def valid_node(self, node):
        if not self.boundary.contains_point((node.x, node.y)):
            return False

        for obstacle in self.obstacles:
            if obstacle.contains_point((node.x, node.y)):
                return False
                
        return True


    def create_segment_path(self, node, visited_nodes):
        if node.parent_key is None:
            return [ [node.x, node.y] ]

    
        return [[node.x, node.y]] + self.create_segment_path(visited_nodes[node.parent_key], visited_nodes)


    def boundary_path(self):
        xCoords, yCoords = self.map.boundary()
        return Path(np.array(list(zip(xCoords,yCoords))))


    def obstacle_path(self):
        x_coordinates, y_coordinates, radii = self.map.obstacles()
        obstacles = []

        for i in range(len(radii)):
            obstacles.append(Path.circle((x_coordinates[i],y_coordinates[i]), radii[i]))
        
        return obstacles


    def get_motion_model(self):
        # dx, dy, cost
        motion = [[0, self.base, self.base],                               # up
                  [0, -self.base, self.base],                              # down
                  [self.base, 0, self.base],                               # right
                  [-self.base, 0, self.base],                              # left
                  [self.base, self.base, math.sqrt(2*self.base**2)],       # top right
                  [-self.base, self.base, math.sqrt(2*self.base**2)],      # top left
                  [self.base, -self.base, math.sqrt(2*self.base**2)],      # bottom right
                  [-self.base, -self.base, math.sqrt(2*self.base**2)]]     # bottom left

        return motion


    def base_rounding(self, x, y, base):
        return base * round(x/base),  base * round(y/base)


    def lowest_cost_node(self, x_target, y_target, priority_queue):
        keys = list(priority_queue.keys())
        lowest_cost = None

        for key in keys:
            node = priority_queue[key]
            cost = self.calculate_cost(x_target, y_target, node)

            if lowest_cost == None or cost < lowest_cost:
                lowest_cost = cost

        for key in keys:
            node = priority_queue[key]
            cost = self.calculate_cost(x_target, y_target, node)
            
            if cost == lowest_cost:
                return priority_queue.pop(key)

    def calculate_cost(self, x_target, y_target, node):
        return node.cost + self.target_distance(x_target, y_target, node.x, node.y)