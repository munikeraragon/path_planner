# This script will have a function that spits out planning data

"""

Grid based Dijkstra planning

author: Muniker Aragon

"""


'''     Descriptipn

    - Helps you find the shortest path in a graph.
    - The vertices of the graph can be locations and the edges the distance between them.
    - The edges can also be viewed as having a --cost--, which is used to find the shortest or 
      the most --cost-- eficient path.  
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

class Dijkstra:
    def __init__(self, loader):
        self.map = loader 
        self.visited = [] # store visited nodes
        self.priority_queue = [] # store nodes that need to be visited

        # starting index
        self.x_start = 0
        self.y_start = 0

        # grid size
        self.x_min = 0
        self.x_max = 4
        self.y_min = 0
        self.y_max = 4

    class Node:
        def __init__(self, x, y, cost, parent_node):
            self.x = x
            self.y = y
            self.cost = cost
            self.parent_node = parent_node


    def plan(self):
        # add starting node to priority queue
        priority_queue.append(Node(self.x_start, y_start, 0, -1))

        # inspect neighbors node. Calculate distance of the neighbors to the starting node
        # edge_distance + parent_distance
        while len(priority_queue) not 0:
            # pop from priority queue
            # node = pop 
            inspect_neighbords(node)
    
    def inspect_neighbors(self, node):
        # inspect adjacent neighbords
        up = [node.x, node.y+1]
        down = [node.x, node.y-1]
        left = [node.x-1, node.y]
        right = [node.x+1, node.y]
        adjacent_nodes = [up, down, left, right]

        for neighbords in adjacent_set:
            if is_valid(neighbord):
                cost = node.cost + 1
                if is_visited(neighbord):
                    # check if cost is less and replace in visited
                else:
                    # add node to visite node
                # add node to priority queue

    def is_valid(self, neighbord):
        if inside_grid(neighbord) and not obstacle(neighbord): 
            return neighbord
        else:
            return None
    def inside_grid(self, node):
        return node.x < x_max and node.x > x_min and node.y < y_max and node.y > y_min
    def obstacle(self, node):





    def simulate(self, plt):
        # begin to run simulation
        for i in range(0, 1000, 100):
            print('ploting')
            plt.plot(i, i, 'xk')
            plt.pause(2)
