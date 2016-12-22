# -*- coding: utf-8 -*-
import networkx as nx
from math import sqrt


class Circle():
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def move(self, new_x, new_y):
        self.center_x = new_x
        self.center_y = new_y

    def equation(self, x, y):
        '''
        circle equation
        :param x:
        :param y:
        :return: zero if x, y on the edge of the circle, minus value if x,y in the circle, plus otherwise
        '''
        return (x - self.center_x) * (x - self.center_x) \
               + (y - self.center_y) * (y - self.center_y) \
               - self.radius * self.radius


def get_pos_dict(graph):
    pos = {}
    for n in graph.nodes_iter():
        pos[n] = graph.node[n]['pos']
    return pos


def add_node_with_pos(graph, n, x, y, **kwargs):
    graph.add_node(n, kwargs)
    graph.node[n]['pos'] = (x, y)


def distance(graph, n1, n2):
    pos1 = graph.node[n1]['pos']
    pos2 = graph.node[n2]['pos']
    return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))


def center_pos(graph):
    pos_x = [graph.node[n]['pos'][0] for n in graph.nodes_iter()]
    pos_y = [graph.node[n]['pos'][1] for n in graph.nodes_iter()]
    c_x = int((min(pos_x) + max(pos_x)) / 2)
    c_y = int((min(pos_y) + max(pos_y)) / 2)
    return c_x, c_y


def nodes_in_circle(graph, circle):
    '''
    search nodes of the graph inside the circle made by the x, y, and radius
    :param graph:
    :type circle: Circle
    :return: list of nodes inside the circle
    '''
    covered_nodes = []
    for n in graph.nodes_iter():
        pos_x, pos_y = graph.node[n]['pos']
        if circle.equation(pos_x, pos_y) <= 0: # pos_x, y inside or on the edge of the circle
            covered_nodes.append(n)
    return covered_nodes


def circle_pos_has_most_nodes(graph, radius):
    '''
    the center position of circle that has the most nodes other than position.
    the position is one of graph's nodes' position
    :param graph:
    :param radius:
    :return (x, y):
    '''
    covered_nodes = 0
    retpos = (0, 0)
    circle = Circle(0, 0, radius)
    for n in graph.nodes():
        x, y = graph.node[n]['pos']
        circle.move(x, y)
        t = len(nodes_in_circle(graph, circle))
        if t > covered_nodes:
            covered_nodes = t
            retpos = (x, y)
    return retpos