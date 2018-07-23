#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/01

@author: Hitoshi Kono
'''
import time
import threading
import logging
import csv
from datetime import datetime

from scipy import *

import config
import learning
import world
import environment
import graph
import world

import scipy
import numpy

import matplotlib.pyplot as plt
import matplotlib.gridspec as gsc

'''
This parameter is controlled start/stop of the simulation,
and to cooperate the pygame's key input program in the environment module.
'''
RUNNING = False
DATE = datetime.now().strftime("%Y%m%d_%H%M%S")
POLNUM = ("%d"%config.POLICY_NUMBER)

class Agent(threading.Thread):

    '''
    Agent (instance) decleration, you can add the any agent in this area.
    '''
    hunter1 = learning.Learning()


    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)

    def __init__(self):
        super(Agent, self).__init__()


    '''
    Deployment (reset) the agent and goal position in the world.
    If you add the other type of agent, you have to add in the following
    statements.
    '''
    def resetWorld(self, tmpState):
        world.GRID[ world.START[1] ][ world.START[0] ] = environment.AGT
        world.GRID[ world.GOAL[1] ][ world.GOAL[0] ] = environment.GOAL
        tmpState[:] = world.START   # Copy the default position from list of START coordinates


    '''
    This method composes the episodes (e.g. [1,2,3,4, ... ,n]) and steps (e.g. [y1,y2,y3,...ym]).
    First array's structure is two rows matrix, so second statement is processed it
    to transposed matrix like bellow:
    1, y1
    2, y2
    3, y3
    4, y4
    -
    -
    -
    n, ym
    Moreover, if the data is NumPy array, we can put the csv write function directory.
    '''
    def loggerStepEpisode(self, filename, episodes, steps):
        tmpSteps = []
        for i in range(len(episodes)):
             tmpSteps.append([episodes[i],steps[i]])
        with open(filename,mode="w",buffering=-1) as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(tmpSteps)
        return 1


    '''
    Q-taable logger. This method using Numpy's function, so file format is not CSV.
    Take care!
    '''
    def loggerQtable(self, filename, policy):
        tmpdate = []
        tmp_f = 0
        tmp_g = 0
        tmp_h = 0
        tmp_i = 0
        tmp_e = 0
        tmp_j = 0
        tmp_k = 0
        tmp_l = 0
        tmp_m = 0
        
        # x:i y:j a:k
        for i in range(1,world.GRID.shape[0]-1):
           for j in range(1,world.GRID.shape[1]-1):
               #マップチップ番号は0=路,1=壁なので注意(高桑さんのデータとは違う)
                try:
                   tmp_f = world.GRID[j-1][i-1]
                except IndexError:
                    print("f is out of index")
                try:
                   tmp_g = world.GRID[j-1][i]
                except IndexError:
                    print("g is out of index")
                try:
                   tmp_h = world.GRID[j-1][i+1]
                except IndexError:
                    print("h is out of index")
                try:
                   tmp_i = world.GRID[j][i-1]
                except IndexError:
                    print("i is out of index")
                try:
                   tmp_e = world.GRID[j][i]
                except IndexError:
                    print("e is out of index")
                try:
                   tmp_j = world.GRID[j][i+1]
                except IndexError:
                    print("j is out of index")
                try:
                   tmp_k = world.GRID[j+1][i-1]
                except IndexError:
                    print("k is out of index")
                try:
                   tmp_l = world.GRID[j+1][i]
                except IndexError:
                    print("l is out of index")
                try:
                   tmp_m = world.GRID[j+1][i+1]
                except IndexError:
                    print("m is out of index")
                for k in range(0,4):
                    #上・右・下・左・静止
                    #print("x:",i,"y:",j,"a:",k,"Q:",policy[i][j][0][0][k],tmp_e,tmp_f,tmp_g,tmp_h,tmp_i,tmp_j,tmp_k,tmp_l,tmp_m)
                    tmpdate.append( [i,j,k,policy[i][j][0][0][k],tmp_e,tmp_f,tmp_g,tmp_h,tmp_i,tmp_j,tmp_k,tmp_l,tmp_m,world.START[0],world.START[1]] )
        with open(filename,mode="w",buffering=-1) as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(tmpdate)
        return 1

    '''
    Method of the learning agent.
    '''
    def learner(self, num):

        '''
        Learning proccess of the agent.
        '''
        while config.NEPISODES <= config.FINISH_EPISODE[num]:
            if RUNNING == True:
                self.hunter1.action(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, self.hunter1.REUSEPOLICY, self.hunter1.ACT)
                config.NSTEPS = config.NSTEPS + 1

                if (self.hunter1.STATE == world.GOAL) == True:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, config.REWARD_POSITIVE[num])
                    config.STEPS.append(config.NSTEPS)          # Append to list the number of steps
                    config.EPISODES.append(config.NEPISODES)    # Append to list the number of episodes
                    config.NEPISODES = config.NEPISODES + 1     # Add one to number of episodes
                    config.NSTEPS = 0                           # Set default value as 0 step
                    config.TREWARD = config.TREWARD + config.REWARD_POSITIVE[num] # Final sum of the goal reward
                    config.TREWARDS.append(config.TREWARD)      # Append to list the total reward
                    config.TREWARD = 0
                    self.resetWorld(self.hunter1.STATE)              # Reset the coordinates
                elif self.hunter1.ACT[2] < 0:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, config.REWARD_NEGATIVE[num])
                    config.TREWARD = config.TREWARD + config.REWARD_NEGATIVE[num]
                else:
                    self.hunter1.updateQ(self.hunter1.STATE, self.hunter1.OLD_STATE, self.hunter1.POLICY, num, self.hunter1.ACT, config.REWARD_ZERO)
                    config.TREWARD = config.TREWARD + config.REWARD_ZERO

                time.sleep(config.TIMESTEP)

            else:
                time.sleep(0.1)                                 # Sleeping time of wait for start


    '''
    Described following codes are execution codes in the thread.
    '''
    def run(self):
        logging.info('Thread start')

        # Deploying the agent and goal.
        self.resetWorld(world.START)

        # Call the learning function based on selected type of learning
        # First call is Reinforcement Learning
        if config.LEARNING_MODE == 1:
            fileStepsRL = "./source/steps_" + POLNUM + "_" + DATE + ".csv"
            fileQtableRL = "./source/qtable_" + POLNUM + "_" + DATE + ".csv"
            logging.info('Reinforcement learning (Source task) start')
            self.learner(0)
            logging.info('Source task is terminated')
            self.loggerStepEpisode(fileStepsRL, config.EPISODES, config.STEPS)
            self.loggerQtable(fileQtableRL, self.hunter1.POLICY)
            # Declaration of subfigures with gridspec
            """
            graphname = "./source/graphs_" + DATE + ".png"
            logging.info("graphname %s",graphname)
            gs = gsc.GridSpec(2, 7)
            fig = plt.figure(figsize=(10,7))
            graph1 = fig.add_subplot(gs[1, 0:7])
            graph2 = fig.add_subplot(gs[0, 0:4])
            # Setting of pyplot
            graph1.set_title("Learning curve")
            graph1.set_ylabel("Number of steps")
            graph1.set_xlabel("Number of episodes")
            graph2.set_title("Transition of total rewards")
            graph2.set_ylabel("Total rewards")
            graph2.set_xlabel("Number of episodes")
            # Adjust to fit amoung graphs
            fig.tight_layout()
            # Loop of representation of graphs in plot window
            MAX_NEPISODE = config.FINISH_EPISODE[0]  # Reinforcement learning
            logging.info("MAX_NEPISODE %s",MAX_NEPISODE)
            graph1.plot(config.EPISODES, config.STEPS)
            graph2.plot(config.EPISODES, config.TREWARDS)
            plt.show()
            """
        # Second call is Transfer Learning
        elif config.LEARNING_MODE == 2:
            fileStepsTL = "./target/steps_" + POLNUM + "_" + DATE + ".csv"
            fileQtableTL = "./target/qtable_" + POLNUM + "_" + DATE + ".csv"
            logging.info('Transfer learning (Target task) start')
            self.learner(1)
            logging.info('Target task is terminated')
            self.loggerStepEpisode(fileStepsTL, config.EPISODES, config.STEPS)
            self.loggerQtable(fileQtableTL, self.hunter1.POLICY)
        else:
            logging.warning ('mode error')
