#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
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


def move_redundant_nodes_to_uncovered_area(MA):
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


def print_stat(monitoring_area):
    rn = len(monitoring_area.redundant_nodes())
    uc = sum([n.number_of_nodes() for n in monitoring_area.uncovered_area()])
    print 'sensing range: ', monitoring_area.wsn_prop.sensing_range,
    print 'redundant nodes: ', rn, 'uncovered_ipoints: ', uc, uc*100/monitoring_area.ipoints.number_of_nodes()


if __name__ == '__main__':
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 5

    nodes = make_nodes_randomly(prop.width, prop.height, 23)

    # EXP1, variable grid_size, sensing_range
    # for gs in range(10, 0, -1):
    #     print gs,
    # print
    #
    # for sr in range(5, 25):
    #     prop.sensing_range = sr
    #     # EXP1: for granularity of the grid_size
    #     print sr,
    #     for gs in range(10, 0, -1):
    #         prop.grid_size = gs
    #         MA = wsn.MonitoringArea(prop)
    #         for n in nodes:
    #             MA.add_node(n[0], n[1], n[2])
    #         #print_stat(MA)
    #         uc = sum([n.number_of_nodes() for n in MA.uncovered_area()])
    #         uc = uc*100/MA.ipoints.number_of_nodes()
    #         print uc,
    #     print

    # EXP2, variable grid_size, variable nodes
    prop.sensing_range = 15
    x_pos = []
    y_pos = []
    uc_list = []
    for nn in range(20, 50, 5):
        nodes = make_nodes_randomly(prop.width, prop.height, nn)
        print nn,
        for gs in range(10, 0, -1):
            prop.grid_size = gs
            MA = wsn.MonitoringArea(prop)
            for n in nodes:
                MA.add_node(n[0], n[1], n[2])
            # print_stat(MA)
            uc = sum([n.number_of_nodes() for n in MA.uncovered_area()])
            uc = uc * 100 / MA.ipoints.number_of_nodes()
            x_pos.append(nn)
            y_pos.append(gs)
            uc_list.append(uc)
            print uc,
        print

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(x_pos, y_pos, [0]*len(x_pos), 1, 0.5, uc_list, color='b')
    plt.show()


    # MA = wsn.MonitoringArea(prop)
    # for n in nodes:
    #     MA.add_node(n[0], n[1], n[2])
    #
    # print_stat(MA)
    #
    # #MA.draw_area()
    # #plt.show()
    #
    # move_redundant_nodes_to_uncovered_area(MA)
    #
    # print_stat(MA)
    #
    # #MA.draw_area()
    # #plt.show()
    #
    # MA2 = wsn.MonitoringArea(prop)
    # for n in nodes:
    #     MA2.add_node(n[0], n[1], n[2])
    # print_stat(MA2)