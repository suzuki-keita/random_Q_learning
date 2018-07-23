#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/04

@author: Hitoshi Kono
'''

from scipy import *

'''
Environmental varialbles which are not depend on
the kind of the learning.
You must be set the coordinates based on window coordinates
'''
START = [10,1]
GOAL = [1,10]

'''
Grid world structure with numpy.array
You should match the plase of number '3' with
above declerations START_X and START_Y.

'''
GRID = array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
              [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
              [1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
              [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
              [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
              [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
