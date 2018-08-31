#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/04

@author: Hitoshi Kono
'''

import numpy as np

'''
Environmental varialbles which are not depend on
the kind of the learning.
You must be set the coordinates based on window coordinates
'''
START = [11,1]
GOAL = [1,11]

'''
Grid world structure with numpy.array
You should match the plase of number '3' with
above declerations START_X and START_Y.

'''
GRID = np.array([[3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3],
                 [3 ,2 ,2 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,3 ,2 ,3],
                 [3 ,2 ,2 ,2 ,3 ,3 ,3 ,3 ,3 ,2 ,3 ,2 ,3],
                 [3 ,2 ,3 ,2 ,2 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,3],
                 [3 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,3 ,3 ,3 ,2 ,3],
                 [3 ,2 ,3 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,3],
                 [3 ,2 ,3 ,3 ,2 ,2 ,3 ,2 ,2 ,2 ,3 ,2 ,3],
                 [3 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,3 ,2 ,3],
                 [3 ,2 ,3 ,2 ,3 ,2 ,3 ,2 ,3 ,2 ,3 ,3 ,3],
                 [3 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,3 ,2 ,2 ,2 ,3],
                 [3 ,3 ,3 ,3 ,3 ,2 ,3 ,3 ,3 ,2 ,3 ,3 ,3],
                 [3 ,2 ,2 ,2 ,2 ,2 ,3 ,2 ,2 ,2 ,2 ,2 ,3],
                 [3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3]])
