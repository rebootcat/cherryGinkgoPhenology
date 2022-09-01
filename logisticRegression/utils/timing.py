# -*- coding: UTF-8 -*-
"""
@author:rebootcat
@file:timing.py.py
@time:2022/09/01
@target: 
"""
from scipy import stats, sqrt, mean
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, r2_score
from scipy.optimize import curve_fit
import numpy as np


def calc_timing(x_list, y_list):
    """
    all necessary packages are imported in this file.
    the core algorithm is private assets of research team,
    please contact corresponding author for license
    :param x_list:
    :param y_list:
    :return:
    """
    tl, tr = None, None
    x_max = max(x_list)
    x_min = min(x_list)
    y_max = np.max(y_list)

    b_index = np.where(y_list == y_max)[0].tolist()
    bx = []
    for index in b_index:
        bx.append(x_list[index])
    b = -1 * (round(sum(bx) / len(bx)))
    c = max(y_list)
    d = min(y_list)
    print("b:{} c:{} d:{} x_max:{}".format(b, c, d, x_max))
    distance = []
    for xb in x_list:
        dis = abs(-1 * b - xb)
        distance.append(dis)
    x_index = distance.index((min(distance)))

    x_left = np.array(x_list[:x_index + 1])
    y_left = np.array(y_list[:x_index + 1])
    x_right = np.array(x_list[x_index:])
    y_right = np.array(y_list[x_index:])
    return tl, tr


def function_l(x, a):
    global b, c, d
    y = (c / (1 + np.exp(-1 * a * (x + b)))) + d
    return y


def function_r(x, a):
    global b, c, d
    y = (c * np.exp(a * (x + b)) / (1 + np.exp(a * (x + b)))) + d
    return y
