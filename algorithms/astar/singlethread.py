from matplotlib.path import Path
import numpy as np
import math

class Astar:
    def __init__(self, loader):
        self.map = loader
        self.visited_nodes = {}
        self.priority_queue = {}
        self.base = 20

        self.motion = self.get_motion_model()
        self.boundary = self.boundary_path()
        self.obstacles = self.obstacle_path()


        # starting coordinate
        self.x_start, self.y_start = self.map.start_point()
        self.x_start, self.y_start = self.base_rounding(self.x_start, self.y_start, self.base)
        
        # target coordinate
        self.x_target, self.y_target = 300, 800
        self.x_target, self.y_target = self.base_rounding(self.x_target, self.y_target, self.base)



    class Node:
        def __init__(self, x, y, cost, parent_key):
            self.x = x
            self.y = y
            self.cost = cost
            self.parent_key = parent_key
        
    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.parent_key)


    def run(self, plt):
        x_coords, y_coords = self.map.way_points()
        way_points = np.array(list(zip(x_coords, y_coords)))


        for coord in way_points:
            x = coord[0]
            y = coord[1]

            self.x_target, self.y_target = self.base_rounding(coord[0], coord[1], self.base)
            self.run_segment(plt)


            # updating starting position
            self.x_start = self.x_target
            self.y_start = self.y_target

            # reseting algoritm storage
            self.visited_nodes = {}
            self.priority_queue = {}
        
        print('Finished algorithim')



    
    def run_segment(self, plt):
        print('Running Segment')

        start_node = self.Node(self.x_start, self.y_start, 0, None) 
        start_key = str(self.x_start) + str(self.y_start)
        
        self.priority_queue[start_key] = start_node


        while len(self.priority_queue) != 0:
            current_node = self.lowest_cost_node()

            self.inspect_neighbords(current_node)

            # plot visited node
            #plt.plot(current_node.x, current_node.y, 'xk')
            #plt.pause(0.001)

            # check if target coordinate has been reached
            if current_node.x == self.x_target and current_node.y == self.y_target:
                self.plot_final_route(plt, current_node)
                print('Target coordinate has been reached')
                return 

        

    def inspect_neighbords(self, node):
        parent_key = str(node.x) + str(node.y)

        # create neighbord Nodes using the motion model
        for move_x, move_y, move_cost in self.motion:
            neighbord = self.Node(node.x+move_x, node.y+move_y, node.cost+move_cost, parent_key)

            if self.valid_node(neighbord):
                key = str(neighbord.x) + str(neighbord.y)

                if key in self.priority_queue:
                    if neighbord.cost < self.priority_queue[key].cost:
                        self.priority_queue[key] = neighbord
                

                if key not in self.visited_nodes and key not in self.priority_queue:
                    self.priority_queue[key] = neighbord  

        self.visited_nodes[parent_key] = node


    def target_distance(self, x, y):
        return math.sqrt(pow(self.x_target-x,2) + pow(self.y_target-y, 2))


    def valid_node(self, node):
        if not self.boundary.contains_point((node.x, node.y)):
            return False

        for obstacle in self.obstacles:
            if obstacle.contains_point((node.x, node.y)):
                return False
                
        return True


    def plot_final_route(self, plt, node):
        if node.parent_key is None:
            return

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


    def lowest_cost_node(self):
        keys = list(self.priority_queue.keys())
        lowest_cost = None

        for key in keys:
            node = self.priority_queue[key]
            cost = self.calculate_cost(node)

            if lowest_cost == None or cost < lowest_cost:
                lowest_cost = cost

        for key in keys:
            node = self.priority_queue[key]
            cost = self.calculate_cost(node)
            
            if cost == lowest_cost:
                return self.priority_queue.pop(key)


    def calculate_cost(self, node):
        return node.cost + self.target_distance(node.x, node.y)

    def base_rounding(self, x, y, base):
        return base * round(x/base),  base * round(y/base)