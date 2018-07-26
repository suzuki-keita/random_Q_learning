#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/08/31

@author: Hitoshi Kono
'''
import sys
import time
import threading
import logging
import pygame

import config
import agent
#import scope
import environment
import graph
from environment import *

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)
    logging.info('Threads start')

    '''
    Selecting of the required threads
    '''
    th1 = agent.Agent();                    # Learning
    if config.DIMENSION == 2:
        th2 = environment.Environment();    # PyGame (2D)
    elif config.DIMENSION == 3:
        #th3 = scope.Scope();             # PyOpenGL (3D)
        pass
    else:
        logging.warning('Error of const.DIMENSION')
        logging.info('Simulation shutting down...')
        sys.exit()
    #th4 = graph.Graph();                    # MatPlotLib

    '''
    Starting proccess of the threads
    '''

    th1.start()
    if config.DIMENSION == 2:
        th2.start()
    elif config.DIMENSION == 3:
        #th3.start()
        pass
    #th4.start()

    '''
    PyGame control with key event function
    '''
    pygame.init()
    
    while config.TERMINATE == True:
        for event in pygame.event.get():        # Input of keyboard
            if event.type == pygame.QUIT:       # PyGame quit proccess
                pygame.quit()
                config.TERMINATE = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 'ESC' press, termination of the pygame
                    pygame.quit()
                    config.TERMINATE = False
                elif event.key == pygame.K_s:     # 's' press, start or stop
                    agent.RUNNING = not agent.RUNNING
                elif event.key == pygame.K_t:   # 't' press, non-drawing and drawing is changed
                    environment.DRAW_SWITCH = not environment.DRAW_SWITCH
        pygame.time.wait(10)



    logging.info('All threads are terminated')
