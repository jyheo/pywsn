#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import networkx as nx
import matplotlib.pyplot as plt
import pgrapy as pg
import wsn


def make_nodes_randomly(width, height, num_of_nodes):
    nodes = []
    for s in range(num_of_nodes):
        x = int(random.random() * width)
        y = int(random.random() * height)
        nodes.append([s, x, y])
    return nodes


def print_stat(monitoring_area):
    rn = len(monitoring_area.redundant_nodes())
    uc = sum([n.number_of_nodes() for n in monitoring_area.uncovered_area()])
    print 'redundant nodes: ', rn, 'uncovered_ipoints: ', uc


if __name__ == '__main__':
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 3

    nodes = make_nodes_randomly(prop.width, prop.height, 33)

    MA = wsn.MonitoringArea(prop)
    for n in nodes:
        MA.add_node(n[0], n[1], n[2])

    print_stat(MA)

    MA.draw_area()
    plt.show()

    rn = list(MA.redundant_nodes())
    uncovered_area_graphs = MA.uncovered_area()
    uncovered_area_graphs = sorted(uncovered_area_graphs, key=len, reverse=True)
    for n in rn: # for every node in redundant nodes
        if len(uncovered_area_graphs) == 0:
            break
        g = uncovered_area_graphs[0]
        new_x, new_y = pg.circle_pos_has_most_nodes(g, prop.sensing_range)
        MA.move_node(n, new_x, new_y)
        print 'move_node ', n, new_x, new_y

        covered_nodes = pg.nodes_in_circle(g, pg.Circle(new_x, new_y, prop.sensing_range))
        g.remove_nodes_from(covered_nodes)
        sub = nx.connected_component_subgraphs(g, copy=True)
        del uncovered_area_graphs[0]
        uncovered_area_graphs.extend(sub)
        uncovered_area_graphs = sorted(uncovered_area_graphs, key=len, reverse=True)

    print_stat(MA)

    MA.draw_area()
    plt.show()
