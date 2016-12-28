#!/usr/bin/python
# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

color_tuples = [(255,128,128), (255,160,128), (255,255,152), (152,255,152), (128,255,208), (128,255,255),
                (128,160,255), (128,128,255),  (192,128,255), (255,128,255)]


def colors_str():
    return ['#%02x%02x%02x' % (t[0], t[1], t[2]) for t in color_tuples]


def chart_3d(data, labels = None):
    '''
    draw 3d chart using data
    :param data: list of tuples (x, y, z)
    :return: void
    '''
    x_val = sorted(set([t[0] for t in data]))
    y_val = sorted(set([t[1] for t in data]))
    d = max(len(x_val), len(y_val))
    dx = float(max(x_val) - min(x_val)) / d * 0.7
    dy = float(max(y_val) - min(y_val)) / d * 0.7

    x_pos = [t[0] - dx / 2 for t in data]
    y_pos = [t[1] - dy / 2 for t in data]
    z_height = [t[2] for t in data]

    color_tmp = colors_str()
    num = len(x_pos)
    colors = color_tmp * (num / len(color_tmp)) + color_tmp[:num % len(color_tmp)]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if labels is not None:
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
    ax.bar3d(x_pos, y_pos, [0]*len(x_pos), dx, dy, z_height, color=colors)
    plt.show()


def chart_lines(xdata, data, labels=None, markers=None, legend_labels=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for d in range(len(data)):
        if markers and legend_labels:
            ax.plot(xdata, data[d], marker=markers[d], label=legend_labels[d])
        else:
            ax.plot(xdata, data[d])
    if labels is not None:
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
    ax.legend(loc=2)
    plt.show()
