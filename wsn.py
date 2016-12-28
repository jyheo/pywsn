#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from math import sqrt
from math import ceil
from math import floor
import networkx as nx
import pgrapy as pg


class Properties:
    def __init__(self):
        self.sensing_range = 13
        self.wireless_range = 25


class MonitoringArea:
    def __init__(self, properties):
        self.wsn_prop = properties
        self.width = properties.width
        self.height = properties.height
        self.grid_size = properties.grid_size
        self.ipoints = nx.Graph()
        self.nodes = nx.Graph()
        self.__generate_interesting_points()

    def __generate_interesting_points(self):
        yrange = range(0, self.height, self.grid_size)
        ynum = len(yrange)
        for y in yrange:
            for x in range(0, self.width, self.grid_size):
                index = x + y * ynum
                pg.add_node_with_pos(self.ipoints, index, x, y, covered_nodes=set())
                if x > 0:
                    prev_idx = (x - self.grid_size) + y * ynum
                    self.ipoints.add_edge(prev_idx, index)
                if y > 0:
                    prev_idx = x + (y - self.grid_size) * ynum
                    self.ipoints.add_edge(prev_idx, index)

    def covered_ipoints(self):
        covered_ipoints = set()
        for n in self.nodes.nodes_iter():
            covered_ipoints.update(self.nodes.node[n]['covered_ipoints'])
        uncovered_ipoints = set(self.ipoints.node).difference(covered_ipoints)
        return covered_ipoints, uncovered_ipoints

    def __more_covered_node(self, ip):
        covered_nodes = list(self.ipoints.node[ip]['covered_nodes'])
        covered_ipoints_num = [len(self.nodes.node[c]['covered_ipoints']) for c in covered_nodes]
        m = covered_ipoints_num.index(max(covered_ipoints_num))
        return covered_nodes[m]

    def significant_nodes(self):
        significant_nodes = set()
        for ip in self.ipoints.nodes_iter():
            if len(self.ipoints.node[ip]['covered_nodes']) >= 1:
                cn = set(self.ipoints.node[ip]['covered_nodes'])
                if len(cn.intersection(significant_nodes)) == 0:
                    n = self.__more_covered_node(ip)
                    significant_nodes.add(n)
        return significant_nodes

    def redundant_nodes(self):
        sn = self.significant_nodes()
        return set(self.nodes.node).difference(sn)

    def uncovered_area(self):
        ip_c = self.ipoints.copy()
        for n in ip_c.nodes():
            if len(ip_c.node[n]['covered_nodes']) >= 1:
                ip_c.remove_node(n)
        return nx.connected_component_subgraphs(ip_c, copy=True)

    def draw_area(self):
        # draw interesting points
        nx.draw_networkx_nodes(self.ipoints, pos=pg.get_pos_dict(self.ipoints),
                node_color='g', node_size=10, alpha=0.5)
        #nx.draw_networkx_nodes(self.nodes, pos=pg.get_pos_dict(self.nodes), node_size=10000, alpha=0.3)
        cip, ucip = self.covered_ipoints()
        sn = self.significant_nodes()
        nx.draw_networkx_nodes(self.ipoints, pos=pg.get_pos_dict(self.ipoints), nodelist=ucip, node_color='y', node_size=100, alpha=1.0)

        nx.draw_networkx_nodes(self.nodes, pos=pg.get_pos_dict(self.nodes), node_color='b', alpha=0.5)
        nx.draw_networkx_nodes(self.nodes, pos=pg.get_pos_dict(self.nodes), nodelist=sn, node_color='r')

    def __add_edges(self, new_s):
        for s in self.nodes.nodes_iter():
            if self.wsn_prop.wireless_range >= pg.distance(self.nodes, s, new_s):
                self.nodes.add_edge(s, new_s)

    def __covered_ipoints(self, x, y):
        covered_ipoints = set()
        if (y - self.wsn_prop.sensing_range) % self.grid_size != 0:
            ceil_ = 1
        else:
            ceil_ = 0
        yfrom = max([0, ((y - self.wsn_prop.sensing_range) / self.grid_size + ceil_) * self.grid_size])
        yto = min([(y + self.wsn_prop.sensing_range) / self.grid_size * self.grid_size + 1, self.height])
        ynum = len(range(0, self.height, self.grid_size))
        for yy in range(yfrom, yto, self.grid_size):
            xsqrt = sqrt(self.wsn_prop.sensing_range * self.wsn_prop.sensing_range - (yy - y) * (yy - y))
            xfrom = max([int(ceil(x - xsqrt)) / self.grid_size * self.grid_size, 0])
            xto = min([int(floor(x + xsqrt)) / self.grid_size * self.grid_size + 1, self.width])
            for xx in range(xfrom, xto, self.grid_size):
                idx = xx + yy * ynum
                covered_ipoints.add(idx)
        return covered_ipoints

    def add_node(self, s, x, y):
        pg.add_node_with_pos(self.nodes, s, x, y, covered_ipoints=set())
        self.__add_edges(s)
        ci = self.__covered_ipoints(x, y)
        for ip in ci:
            self.ipoints.node[ip]['covered_nodes'].add(s)
        self.nodes.node[s]['covered_ipoints'] = ci

    def remove_node(self, s):
        for ip in self.nodes.node[s]['covered_ipoints']:
            self.ipoints.node[ip]['covered_nodes'].remove(s)
        self.nodes.remove_node(s)

    def move_node(self, s, x, y):
        self.remove_node(s)
        self.add_node(s, x, y)

