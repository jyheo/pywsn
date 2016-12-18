import networkx as nx
from math import sqrt

class PGraph(nx.Graph):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.pos = {}

    def add_node_with_pos(self, n, x, y, **kwargs):
        super(self.__class__, self).add_node(n, kwargs)
        self.node[n]['pos'] = (x, y)
        self.pos[n] = (x, y)

    def remove_node(self, n):
        super(self.__class__, self).remove_node(n)
        del self.pos[n]

    def distance(self, n1, n2):
        pos1 = self.pos[n1]
        pos2 = self.pos[n2]
        return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))

    def center_pos(self, node_set):
        pos_x = [self.node[n]['pos'][0] for n in node_set]
        pos_y = [self.node[n]['pos'][1] for n in node_set]
        c_x = int((min(pos_x) + max(pos_x)) / 2)
        c_y = int((min(pos_y) + max(pos_y)) / 2)
        return c_x, c_y