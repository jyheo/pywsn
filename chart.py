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
    x_pos = [t[0] for t in data]
    y_pos = [t[1] for t in data]
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
    ax.bar3d(x_pos, y_pos, [0]*len(x_pos), 1, 0.5, z_height, color=colors)
    plt.show()
