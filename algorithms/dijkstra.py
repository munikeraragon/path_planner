# This script will have a function that spits out planning data

"""

Grid based Dijkstra planning

author: Muniker Aragon

"""


'''     Descriptipn

    - Dijkstra algorithim finds shortest path in a graph.
    - The vertices of the graph can be locations and the edges the distance between them.
    - The edges can also be viewed as having a --cost--, which is used to find the shortest or 
      the most --cost-- efficient path.  
    - Algorithim will try to find short cuts in the process.
    - I need to create graph model that that represents grid Visual.
'''

'''     Algorithim

    - Algorithim starts at a starting node
    - Keep nodes that have been found but not process in priority queue
    - The node with the smallest distance to the starting point is the first node in the queue.

    - The starting point has a distance of 0, as its distance to itself
    - cost to other nodes is set to infinity, during algo this costs will be inproved
    - the algorithim remembers the shortes path to every node
    - the starting node is added to the priority queue

    -- start --
    - remove first node from priority queue
    - Check all of its neighbors. CHECK CONDITIONS
    - continue until priority queue is empty and there is no more nodes to process


    -- check conditions --
    1) Is the node contained in the priority queue? if so, it the edge leading to it a shortcut.
        yes -> cost of the node is decrease
        no -> check second constion
    2) Has this node been visited?
        no -> added to the priority queue 

'''

''' Algorithim 
    - staring node has a value of 0
    - assume all other nodes have a value of infinity
    - added startng node to priority queue

    - take node with minimal distance from priority queue and process it
    - inspect neighbors node. Calculate distance of the neighbors to the starting node
      edge_distance + parent_distance
    - if node exists in visited_node, update if path is shorter
    - add node to visited_nodes

'''

import math

class Dijkstra:
    def __init__(self, loader):
        self.map = loader 
        self.visited_nodes = {} # store visited nodes
        self.priority_queue = {} # store nodes that need to be visited

        # starting index
        self.x_start = 5
        self.y_start = 5

        # grid size
        self.x_min = 0
        self.x_max = 60
        self.y_min = 0
        self.y_max = 60

        # goal index
        self.x_goal = 20
        self.y_goal = 10

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
        # staring node has with cost of 0
        starting_node = self.Node(self.x_start, self.y_start, 0, None) 
        starting_key = str(self.x_start) + str(self.y_start)
        # add starting node to priority queue
        self.priority_queue[starting_key] = starting_node
        
        while len(self.priority_queue) != 0:
            # take node with minimal distance from priority queue and process it
            keys = list(self.priority_queue.keys())
            current_node = self.priority_queue.pop(keys[0])
            # inspect neighbors node. Calculate distance of the neighbors to the starting node
            self.inspect_neighbords(current_node)

            # plot visited node
            plt.plot(current_node.x, current_node.y, 'xk')
            plt.pause(0.001)

            # check if destination has been reached
            if current_node.x is self.x_goal and current_node.y is self.y_goal:
                self.plot_final_route(plt, current_node)
                print('goal has been reached')
                break

        print('Finished algorithim')

    def inspect_neighbords(self, node):
        parent_key = str(node.x) + str(node.y)
        up = self.Node(node.x, node.y+1, node.cost+1, parent_key)
        down = self.Node(node.x, node.y-1, node.cost+1, parent_key)
        left = self.Node(node.x-1, node.y, node.cost+1, parent_key)
        right = self.Node(node.x+1, node.y, node.cost+1, parent_key)

        top_right = self.Node(node.x+1, node.y+1, node.cost+math.sqrt(2), parent_key)
        top_left = self.Node(node.x-1, node.y+1, node.cost+math.sqrt(2), parent_key)
        bottom_right = self.Node(node.x+1, node.y-1, node.cost+math.sqrt(2), parent_key)
        bottom_left = self.Node(node.x-1, node.y-1, node.cost+math.sqrt(2), parent_key)
        neighbord_nodes = [up, down, left, right, top_right, top_left, bottom_right, bottom_left]

        for neighbord in neighbord_nodes:
            if self.valid_node(neighbord):
                key = str(neighbord.x) + str(neighbord.y)

                if key in self.visited_nodes:                           # check if neighbord has been visited
                    if neighbord.cost < self.visited_nodes[key].cost:   # if cost is less replace node
                        self.visited_nodes[key] = neighbord

                if key not in self.visited_nodes and key not in self.priority_queue:    # if neighbord has not been visited
                    self.priority_queue[key] = neighbord                                # add to priority_queue
                
        # marked node as visited
        self.visited_nodes[parent_key] = node


    def valid_node(self, node):
        within_grid = node.x > self.x_min and node.x < self.x_max and node.y > self.y_min and node.y < self.x_max
        return within_grid


    def plot_final_route(self, plt, node):
        # base case
        if node.parent_key is None:
            return
        # plot node
        plt.plot(node.x, node.y, 'xc')
        plt.pause(0.001)
        self.plot_final_route(plt, self.visited_nodes[node.parent_key])
        

