import networkx as nx
import matplotlib.pyplot as plt
import random
from math import sqrt
from math import pow

sensing_range = 15
wireless_range = 20


class MonitoringArea:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.generate_interesting_points()

    def generate_interesting_points(self):
        self.ipoints = nx.Graph()
        self.ipoints_pos = {}
        index = 0
        for x in range(0, self.width, self.grid_size):
            for y in range(0, self.height, self.grid_size):
                self.ipoints.add_node(index)
                self.ipoints_pos[index] = (x,y)
                index += 1

    def draw_area(self):
        # draw interesting points
        nx.draw(self.ipoints, pos=self.ipoints_pos,
                node_color='g', node_size=10)
        nx.draw(self.nodes, pos=self.nodes_pos)
        nx.draw(self.nodes, pos=self.nodes_pos, node_size=5000, alpha=0.3)


    def __distance(self, pos1, pos2):
        return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))

    def __add_edges(self, new_s, pos):
        for s in self.nodes_pos:
            if wireless_range >= self.__distance(self.nodes_pos[s], pos):
                self.nodes.add_edge(s, new_s)

    def add_nodes_randomly(self, num_of_nodes):
        self.nodes = nx.Graph()
        self.nodes_pos = {}
        for s in range(num_of_nodes):
            x = random.random() * self.width
            y = random.random() * self.height
            self.nodes.add_node(s)
            self.nodes_pos[s] = (x, y)
            self.__add_edges(s, (x,y))



MA = MonitoringArea(100, 100, 2)
MA.add_nodes_randomly(50)
MA.draw_area()

plt.show()





