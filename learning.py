#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/08/31

@author: Hitoshi Kono
'''
import time
import threading
import logging
import random

import config
import world
import environment

import scipy
import numpy

class Learning:

    logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)

    '''
    Memory space declaration for Q-tables
    In this example, thrird and fourth argument is dammy. For memmory test, we are researved 100.
    You can ignore this 100, and normally you can put the zero in the third and fourth argument.
    '''
    POLICY = scipy.zeros((world.GRID.shape[0],world.GRID.shape[1],1,1,5)) # Declaration of the policy space
    STATE = [world.START[0], world.START[1]]                            # Current coordinates (x, y)
    OLD_STATE = [world.START[0], world.START[1]]                        # Old coordinates
    # This list means as follow
    # ACT[0] is current executing action number
    # ACT[1] is latest executed action number
    # ACT[2] is flag of can not move
    ACT = [0, 0, 0]

    '''
    Transfer (reuse) policy declaration
    '''
    if config.LEARNING_MODE == 1:       # When not transfer
        REUSEPOLICY = 0
    elif config.LEARNING_MODE == 2:     # Which menas transfer learning is selected
        fileTransfer = "./policies/qtable_" + "%d"%config.POLICY_NUMBER + ".npz"
        loadingPolicy = numpy.load(fileTransfer)
        REUSEPOLICY = loadingPolicy['savedPolicy']

    '''
    Execute the action based on numerical data without stay action.
    '''
    def execute(self, state, old_state, num):
        if num == 0:        # Go to up
            state[1] = state[1] - 1                       # Move on coordinates
            world.GRID[ old_state[1] ][ old_state[0] ] = 0# Update the grid information in the world
            world.GRID[ state[1]     ][ state[0]     ] = 3
        elif num == 1:      # Go to right
            state[0] = state[0] + 1                       # Move on coordinates
            world.GRID[ old_state[1] ][ old_state[0] ] = 0# Update the grid information in the world
            world.GRID[ state[1]     ][ state[0]     ] = 3
        elif num == 2:      # Go to down
            state[1] = state[1] + 1                       # Move on coordinates
            world.GRID[ old_state[1] ][ old_state[0] ] = 0# Update the grid information in the world
            world.GRID[ state[1]     ][ state[0]     ] = 3
        elif num == 3:      # Go to left
            state[0] = state[0] - 1                       # Move on coordinates
            world.GRID[ old_state[1] ][ old_state[0] ] = 0# Update the grid information in the world
            world.GRID[ state[1]     ][ state[0]     ] = 3

    '''
    Aaction function with collision check with wall and obstacles.
    If the agent collide with something, re select the action.
    '''
    def do_act(self, state, old_state, num):
        # Storing coordinates in old_state
        old_state[0] = state[0]
        old_state[1] = state[1]
        # Action select statements
        if num == 0:        # Go to up
            if (world.GRID[(state[1]-1)][state[0]] == environment.ROAD or world.GRID[(state[1]-1)][state[0]] == environment.GOAL):
                self.execute(state, old_state, num)
                return 0
            else:           # Collision
                return -1
        elif num == 1:      # Go to right
            if (world.GRID[state[1]][(state[0]+1)] == environment.ROAD or world.GRID[state[1]][(state[0]+1)] == environment.GOAL):
                self.execute(state, old_state, num)
                return 0
            else:           # Collision
                return -1
        elif num == 2:      # Go to down
            if (world.GRID[(state[1]+1)][state[0]] == environment.ROAD or world.GRID[(state[1]+1)][state[0]] == environment.GOAL):
                self.execute(state, old_state, num)
                return 0
            else:           # Collision
                return -1
        elif num == 3:      # Go to left
            if (world.GRID[state[1]][(state[0]-1)] == environment.ROAD or world.GRID[state[1]][(state[0]-1)] == environment.GOAL):
                self.execute(state, old_state, num)
                return 0
            else:           # Collision
                return -1
        elif num == 4:      # Go to stay
            return 0
        else:               # Go to stay
            return 0


    '''
    This function calculates selecting probability based on only Q-value.
    This part is Reinforcement learning.
    '''
    def probabilityQ(self, state, policy, v, p):
        total = 0   # Total value for the boltzmann
        for n in range(0,5):
            v[n] = policy[state[0]][state[1]][0][0][n]
        for m in range(0,5):
            total = total + scipy.exp(v[m]/config.BOLTZMANN_TEMP[0])
        for l in range(0,5):
            p[l] = (scipy.exp(v[l]/config.BOLTZMANN_TEMP[0]))/total


    '''
    This method is processed Inter Task Mapping for Transfer Learning.
    '''
    def iTaskMap(self, state, actNum, reusePolicy):
        value = reusePolicy[state[0]][state[1]][0][0][actNum]
        return value


    '''
    This function calculates selecting probability with current policy and reusing policy,
    which menas Transfer tearning.
    '''
    def probabilityT(self, state, policy, reusePolicy, v, p):
        total = 0
        for n in range(0,5):
            v[n] = policy[state[0]][state[1]][0][0][n] + config.TRANSFER_RATE * self.iTaskMap(state, n, reusePolicy)
        for m in range(0,5):
            total = total + scipy.exp(v[m]/config.BOLTZMANN_TEMP[1])
        for l in range(0,5):
            p[l] = (scipy.exp(v[l]/config.BOLTZMANN_TEMP[1]))/total

    '''
    Selecting of the action based on policy
    with boltzmann distribution model.
    x is self.state[0]
    y is self.state[1]
    Also, old_state means the previous coordinates.
    the policy is the Q-talbe data of the agent based on numpy array.
    the num menas that the your selected type of learing Reinforcement or Transfer.
    '''
    def action(self, state, old_state, policy, reusePolicy, act):

        v = scipy.zeros(5)        # List of action values
        p = scipy.zeros(5)        # List of possibilities of action

        act[1] = act[0]           # Storing of executed action to old action

        if config.LEARNING_MODE == 1:       # Reinforcement learning
            self.probabilityQ(state, policy, v, p)
        elif config.LEARNING_MODE == 2:     # Transfer learning
            self.probabilityT(state, policy, reusePolicy, v, p)

        c = random.random()
        if c >= 0.0 and c < p[0]:
            ret = self.do_act(state, old_state, 0)  # Go to up
            act[0] = 0
        elif c >= p[0] and c < (p[0]+p[1]):
            ret = self.do_act(state, old_state, 1)  # Go to right
            act[0] = 1
        elif c >= (p[0]+p[1]) and c < (p[0]+p[1]+p[2]):
            ret = self.do_act(state, old_state, 2)  # Go to down
            act[0] = 2
        elif c >= (p[0]+p[1]+p[2]) and c < (p[0]+p[1]+p[2]+p[3]):
            ret = self.do_act(state, old_state, 3)  # Go to left
            act[0] = 3
        elif c >= (p[0]+p[1]+p[2]+p[3]) and c <= (p[0]+p[1]+p[2]+p[3]+p[4]):
            ret = self.do_act(state, old_state, 4)  # Stay
            act[0] = 4
        else:
            ret = self.do_act(state, old_state, 4)  # Stay (for Error)
            act[0] = 4

        '''
        Reflexive call of action function when the agent can not move.
        If you control the agent behavior which keepes stay when the agent encounter obstacles,
        you have to delete following statement.
        '''
        if ret < 0:
            act[2] = ret
        else:
            act[2] = 0

    '''
    Return the current state which is coordinates
    of the agent in the grid
    '''
    def observ(self):
        pass

    '''
    This method is arg max function of the Q-value, so this returns the action number
    which has maximumu Q-value.
    '''
    def argMaxQ(self, state, policy, nAct):
        tmpValue = scipy.zeros(nAct)
        for i in range (0, nAct):
            tmpValue[i] = policy[state[0]][state[1]][0][0][i]

        tmpMaxValue = 0
        numAct = 0
        for j in range (0, nAct):
            if tmpMaxValue <= tmpValue[j]:
                tmpMaxValue = tmpValue[j]
                numAct = j

        return numAct


    '''
    Updating the Q-value
    '''
    def updateQ(self, state, old_state, policy, num, act, reward):
        maxQact = self.argMaxQ(state, policy, 5)
        TDerror = config.DISCOUNT_RATE[num] * policy[state[0]][state[1]][0][0][maxQact] - policy[old_state[0]][old_state[1]][0][0][act[0]]
        policy[old_state[0]][old_state[1]][0][0][act[0]] = policy[old_state[0]][old_state[1]][0][0][act[0]] + config.LEARNING_RATE[num] * (reward + TDerror)
