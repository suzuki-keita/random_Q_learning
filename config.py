#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017/09/01

@author: Hitoshi Kono
'''

'''
Setup parameters of this simulation.
If you select the '2' as DIMENSION, grid world
is deployed in the environment. On the other hand
If '3' was selected, 3D world is deployed in the
environment
'''
DIMENSION = 2   # 2 or 3

'''
Type of simulation.
1: Reinforcement learning (Source task)
2: Transfer learning (Target task)
'''
LEARNING_MODE = 1   # 1 or 2

'''
Waiting time in each action (step).
If you set this value without 0,
Simulation speed becomes down.
'''
TIMESTEP = 0.0

'''
System variables' declerations
'''
# Experimental parameters
TERMINATE = True

# List for the graphs
NEPISODES = 1   # Do not modify
NSTEPS = 0      # Do not modify
TREWARD = 0     # Do not modify
EPISODES = []
STEPS = []
TREWARDS = []
# From this line, for the learning parameters
LEARNING_RATE = []
DISCOUNT_RATE = []
FINISH_EPISODE = []
BOLTZMANN_TEMP = []
REWARD_POSITIVE = []
REWARD_NEGATIVE = []
REWARD_ZERO = 0

'''
Reinforcement learning parameters
'''
LEARNING_RATE.append(0.1)
DISCOUNT_RATE.append(0.99)
FINISH_EPISODE.append(500)
BOLTZMANN_TEMP.append(0.05)
REWARD_POSITIVE.append(1.0)     # You have to set this value not integer
REWARD_NEGATIVE.append(0.0)     # You have to set this value not integer

'''
Transfer learning parameters
'''
LEARNING_RATE.append(0.1)
DISCOUNT_RATE.append(0.99)
FINISH_EPISODE.append(500)
BOLTZMANN_TEMP.append(0.05)
REWARD_POSITIVE.append(1.0)     # You have to set this value not integer
REWARD_NEGATIVE.append(-1.0)   # You have to set this value not integer

TRANSFER_RATE = 1.0

POLICY_NUMBER = 1
