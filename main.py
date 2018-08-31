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
import make_maze
import world

DEBUG_MODE = 0

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)
    logging.info('Threads start')
    
    if DEBUG_MODE == 0:
        logging.info('MAIN_MODE!')
        for i in range(1,1000):
            mazes = make_maze.Make_maze()
            configs = config.Config()

            world.GRID = mazes.maze
            world.START = mazes.start_grid
            world.GOAL = mazes.goal_grid
            logging.info('%i time',i)

            '''
            Selecting of the required threads
            '''
            th1 = agent.Agent(configs)                    # Learning
            if configs.DIMENSION == 2:
                #th2 = environment.Environment(configs,th1);    # PyGame (2D)
                pass
            elif configs.DIMENSION == 3:
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
            if configs.DIMENSION == 2:
                #th2.start()
                pass
            elif configs.DIMENSION == 3:
                #th3.start()
                pass
            #th4.start()

            '''
            PyGame control with key event function
            '''
            """
            pygame.init()
            while configs.TERMINATE == True:
                for event in pygame.event.get():        # Input of keyboard
                    if event.type == pygame.QUIT:       # PyGame quit proccess
                        pygame.quit()
                        configs.TERMINATE = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # 'ESC' press, termination of the pygame
                            pygame.quit()
                            configs.TERMINATE = False
                        elif event.key == pygame.K_s:     # 's' press, start or stop
                            th1.RUNNING = not th1.RUNNING
                th1.RUNNING = True
                pygame.time.wait(10)
            """
            th1.RUNNING = True
            th1.join()
            logging.info('All threads are terminated')

    elif DEBUG_MODE == 1:
        logging.info('DEBUG_MODE')
        mazes = make_maze.Make_maze()
        configs = config.Config()
        world.GRID = mazes.maze
        world.START = mazes.start_grid
        world.GOAL = mazes.goal_grid

        '''
        Selecting of the required threads
        '''
        th1 = agent.Agent(configs)                    # Learning
        if configs.DIMENSION == 2:
            th2 = environment.Environment(configs,th1);    # PyGame (2D)
            pass
        elif configs.DIMENSION == 3:
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
        if configs.DIMENSION == 2:
            th2.start()
        elif configs.DIMENSION == 3:
            #th3.start()
            pass
        #th4.start()

        '''
        PyGame control with key event function
        '''
        pygame.init()
        while configs.TERMINATE == True:
            for event in pygame.event.get():        # Input of keyboard
                if event.type == pygame.QUIT:       # PyGame quit proccess
                    pygame.quit()
                    configs.TERMINATE = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 'ESC' press, termination of the pygame
                        pygame.quit()
                        configs.TERMINATE = False
                    elif event.key == pygame.K_s:     # 's' press, start or stop                            th1.RUNNING = not th1.RUNNING
                        th1.RUNNING = True
            pygame.time.wait(10)
        th1.join()
        logging.info('All threads are terminated')
