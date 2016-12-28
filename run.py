#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
import pgrapy as pg
import wsn
import chart


def make_nodes_randomly(width, height, num_of_nodes):
    nodes = []
    for s in range(num_of_nodes):
        x = int(random.random() * width)
        y = int(random.random() * height)
        nodes.append([s, x, y])
    return nodes


def move_redundant_nodes_to_uncovered_area(MA, prop):
    rn = list(MA.redundant_nodes())
    uncovered_area_graphs = MA.uncovered_area()
    uncovered_area_graphs = sorted(uncovered_area_graphs, key=len, reverse=True)
    for n in rn: # for every node in redundant nodes
        if len(uncovered_area_graphs) == 0:
            break
        g = uncovered_area_graphs[0]
        new_x, new_y = pg.circle_pos_has_most_nodes(g, prop.sensing_range)
        MA.move_node(n, new_x, new_y)
        #print 'move_node ', n, new_x, new_y

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


def exp1(repeat_count=1):
    '''
    EXP1, various grid_size, various number of nodes
    :return: void
    '''
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 5

    prop.sensing_range = 15

    chart_data = []
    uc_list = []
    for i in range(repeat_count):
        idx = 0
        for nn in range(20, 50, 5): # various number of nodes
            nodes = make_nodes_randomly(prop.width, prop.height, nn)
            print nn,
            for gs in range(10, 0, -1): # various grid size
                prop.grid_size = gs
                MA = wsn.MonitoringArea(prop)
                for n in nodes:
                    MA.add_node(n[0], n[1], n[2])
                # print_stat(MA)
                uc = sum([n.number_of_nodes() for n in MA.uncovered_area()])
                uc = uc * 100 / MA.ipoints.number_of_nodes()
                if i == 0:
                    uc_list.append(uc)
                else:
                    uc_list[idx] += uc
                if i == repeat_count - 1:
                    chart_data.append((nn, gs, uc_list[idx] / repeat_count))
                idx += 1
                print uc,
            print

    chart.chart_3d(chart_data, ('number of nodes', 'grid size', 'uncovered points rate(%)'))


def exp2(repeat_count=1):
    '''
    EXP2, various grid_size, various sensing_range
    :return:
    '''
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 5

    nodes = make_nodes_randomly(prop.width, prop.height, 23)

    chart_data = []
    uc_list = []
    for i in range(repeat_count):
        idx = 0
        for sr in range(5, 25): # various sensing_range
            prop.sensing_range = sr
            print sr,
            for gs in range(10, 0, -1): # various grid size
                prop.grid_size = gs
                MA = wsn.MonitoringArea(prop)
                for n in nodes:
                    MA.add_node(n[0], n[1], n[2])
                uc = sum([n.number_of_nodes() for n in MA.uncovered_area()])
                uc = uc*100/MA.ipoints.number_of_nodes()
                if i == 0:
                    uc_list.append(uc)
                else:
                    uc_list[idx] += uc
                if i == repeat_count - 1:
                    chart_data.append((sr, gs, uc_list[idx] / repeat_count))
                idx += 1
                print uc,
            print

    chart.chart_3d(chart_data, ('sensing range', 'grid size', 'uncovered points rate(%)'))


def exp_visual_demo(move_redundant=True):
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 5

    nodes = make_nodes_randomly(prop.width, prop.height, 20)

    MA = wsn.MonitoringArea(prop)
    for n in nodes:
        MA.add_node(n[0], n[1], n[2])

    print_stat(MA)
    MA.draw_area()
    plt.show()

    if move_redundant:
        move_redundant_nodes_to_uncovered_area(MA, prop)
        print_stat(MA)
        MA.draw_area()
        plt.show()


def opt_placement(prop):
    #optimal number of nodes = prop.width / (sqrt(3) * prop.sensing_range) * prop.height / (1.5 * prop.sensing_range)
    xbegin = sqrt(3) * prop.sensing_range / 2
    ybegin = prop.sensing_range / 2.0
    idx = 0
    nodes = []
    xpos = xbegin
    while xpos < prop.width:
        ypos = ybegin
        while ypos < prop.height:
            nodes.append([idx, int(xpos), int(ypos)])
            idx += 1
            ypos += prop.sensing_range
        xpos += sqrt(3) * prop.sensing_range
    return nodes


def exp3(repeat_count=1, num_of_nodes=25, OPT=False):
    prop = wsn.Properties()
    prop.wireless_range = 30
    prop.sensing_range = 15
    prop.width = 100
    prop.height = 100
    prop.grid_size = 5

    if OPT:
        nodes = opt_placement(prop)
        MA = wsn.MonitoringArea(prop)
        for n in nodes:
            MA.add_node(n[0], n[1], n[2])
        print 'OPT num_of_nodes: ', len(nodes), 'uncovered_ipoints_rate(%): ',\
            sum([n.number_of_nodes() for n in MA.uncovered_area()]) * 100 / MA.ipoints.number_of_nodes()
        return

    before = 0
    after = 0
    for i in range(repeat_count):
        nodes = make_nodes_randomly(prop.width, prop.height, num_of_nodes)

        MA = wsn.MonitoringArea(prop)
        for n in nodes:
            MA.add_node(n[0], n[1], n[2])

        before += sum([n.number_of_nodes() for n in MA.uncovered_area()]) * 100 / MA.ipoints.number_of_nodes()

        move_redundant_nodes_to_uncovered_area(MA, prop)
        after += sum([n.number_of_nodes() for n in MA.uncovered_area()]) * 100 / MA.ipoints.number_of_nodes()

    print 'num_of_nodes: ', num_of_nodes, 'before(%): ', before / repeat_count, 'after(%): ', after / repeat_count
    return before / repeat_count, after / repeat_count


def exp4(repeat_count=1):
    exp3(OPT=True)
    blist = []
    alist = []
    nodes_range = range(15, 27)
    for i in nodes_range:
        b, a = exp3(repeat_count, num_of_nodes=i)
        blist.append(100 - b)
        alist.append(100 - a)
    chart.chart_lines(nodes_range, [alist, blist], ('Number of nodes', 'Covered points rate(%)'), markers='o^',
                      legend_labels=('Proposed', 'Random'))


if __name__ == '__main__':
    exp_visual_demo(move_redundant=True)
    #exp1(repeat_count=10)
    #exp2(repeat_count=10)
    #exp4(repeat_count=20)
