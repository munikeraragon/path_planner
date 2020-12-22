from matplotlib.path import Path
import numpy as np
import math

class Astar:
    def __init__(self, loader):
        self.map = loader
        self.boundary = self.boundary_path()
        self.obstacles = self.obstacle_path()
        self.motion = self.get_motion_model()

        self.visited_nodes = {}
        self.priority_queue = {}

        # starting index
        self.x_start = 750
        self.y_start = 200

        # goal index
        self.x_goal = 600
        self.y_goal = 1000

    class Node:
        def __init__(self, x, y, cost, parent_key):
            self.x = x
            self.y = y
            self.cost = cost
            self.parent_key = parent_key
        
    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.parent_key)

    
    def run(self, plt):
        print('Starting algorithim')

        # create start node
        start_node = self.Node(self.x_start, self.y_start, 0, None)
        start_key = str(self.x_start) + str(self.y_start)

        self.priority_queue[start_key] = start_node  # add node to priority queue

        while len(self.priority_queue) != 0:
            # take node with lowest cost from priority queue
            #current_node = self.lowest_cost_node()
            keys = list(self.priority_queue.keys())
            current_node = self.priority_queue.pop(keys[0])

            # calculate neighbors cost
            self.inspect_neighbords(current_node)

            # plot visited node
            plt.plot(current_node.x, current_node.y, 'xk')
            plt.pause(0.001)

            # check if goal has been reached
            if current_node.x == self.x_goal and current_node.y == self.y_goal:
                self.plot_final_route(plt, current_node)
                print('goal has been reached')
                break

        print('Finished algorithim')

        

    def inspect_neighbords(self, node):
        parent_key = str(node.x) + str(node.y)

        for move_x, move_y, move_cost in self.motion:
            neighbord = self.Node(node.x + move_x,
                             node.y + move_y,
                             node.cost + move_cost,
                             parent_key)

            if self.valid_node(neighbord):
                key = str(neighbord.x) + str(neighbord.y)

                if key in self.priority_queue:                           # check if neighbord exists in priority queue
                    if neighbord.cost < self.priority_queue[key].cost:   # if cost is less replace node
                        self.priority_queue[key] = neighbord
                

                if key not in self.visited_nodes and key not in self.priority_queue:    # if neighbord has not been visited
                    self.priority_queue[key] = neighbord  



    def get_motion_model(self):
        # dx, dy, cost
        motion = [[10, 0, 10],
                  [0, 10, 10],
                  [-10, 0, 10],
                  [0, -10, 10],
                  [-10, -10, math.sqrt(200)],
                  [-10, 10, math.sqrt(200)],
                  [10, -10, math.sqrt(200)],
                  [10, 10, math.sqrt(200)]]

        return motion

    def target_distance(self, x, y):
        # calculate eucledean distance
        p1 = np.array((x, y))
        p2 = np.array((self.x_goal, self.y_goal))
        return np.linalg.norm(p1-p2)

    def valid_node(self, node):
        for obstacle in self.obstacles:
            if obstacle.contains_point((node.x, node.y)):
                return False

        return self.boundary.contains_point((node.x, node.y))


    def plot_final_route(self, plt, node):
        if node.parent_key is None: # base case
            return

        # plot node
        plt.plot(node.x, node.y, 'xc')
        plt.pause(0.001)
        self.plot_final_route(plt, self.visited_nodes[node.parent_key])



    def boundary_path(self):
        xCoords, yCoords = self.map.boundary()
        return Path(np.array(list(zip(xCoords,yCoords))))



    def obstacle_path(self):
        x_coordinates, y_coordinates, radii = self.map.obstacles()
        obstacles = []

        for i in range(len(radii)):
            obstacles.append(Path.circle((x_coordinates[i],y_coordinates[i]), radii[i]))
        
        return obstacles

    def lowest_cost_node(self):
        keys = list(self.priority_queue.keys())
        lowest_cost = None
        optimal_key = None

        for key in keys:
            if not lowest_cost or not optimal_key:
                lowest_cost = self.priority_queue[key].cost
                optimal_key = key
            
            if self.priority_queue[key].cost < lowest_cost:
                lowest_cost = self.priority_queue[key].cost
                optimal_key = key

        return self.priority_queue.pop(optimal_key)
