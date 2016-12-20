# -*- coding: utf-8 -*-
import networkx as nx
from math import sqrt


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


def nodes_covered_by_circle(graph, x, y, radius):
    covered_nodes = []
    for n in graph.nodes_iter():
        pos_x = graph.node[n]['pos'][0]
        pos_y = graph.node[n]['pos'][1]
        rsq = (x - pos_x) * (x - pos_x) + (y - pos_y) * (y - pos_y)
        if rsq <= radius * radius:
            covered_nodes.append(n)
    return covered_nodes
