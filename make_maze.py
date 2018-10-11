#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018/07/29

@author: Keita Suzuki
@mail:15ec067@ms.dendai.ac.jp
'''

import random
import numpy as np
import sys
import logging
import environment
import world

SIZE = world.MAZE_SIZE
BREAK = world.BREAK_WALL

class Make_maze:
    def __init__(self):
        self.maze = np.zeros((SIZE+2, SIZE+2), dtype=int)
        self.wall_stack = []
        self.start_cells = []
        self.start_grid = [0,0]
        self.goal_grid = [SIZE,SIZE]

        if SIZE < 5 or SIZE % 2 == 0:
            logging.info(
                "This prgoram can't make Maze because SIZE is under 5 or Even number.")
            sys.exit()

        #迷路の初期化
        for x in range(0, SIZE+2):
            for y in range(0, SIZE+2):
                if x == 0 or y == 0 or x == SIZE+1 or y == SIZE+1:
                    self.maze[x][y] = environment.WALL
                else:
                    self.maze[x][y] = environment.ROAD
                    if x % 2 == 0 and y % 2 == 0:
                        self.start_cells.append([x, y])

        #壁伸ばしを開始する位置をスタックに積む
        stack_size = len(self.start_cells)
        while stack_size > 0:
            index = random.randrange(stack_size)
            cell = self.start_cells[index]
            self.start_cells.pop(index)
            x = cell[0]
            y = cell[1]
            if self.maze[x][y] == environment.ROAD:
                self.wall_stack = []  # 初期化
                self.ExtendWall(x, y)
            stack_size = len(self.start_cells)

        #迷路をあえて壊して最短経路問題のタスクにする
        for i in range(0, BREAK):
            self.BreakWall()

        #スタート地点・ゴール地点を設定
        tmp = self.GetGrid()
        self.start_grid[0] = tmp[0]
        self.start_grid[1] = tmp[1]
        
        tmp = self.GetGrid(0,self.start_grid[0],self.start_grid[1])
        self.goal_grid[0] = tmp[0]
        self.goal_grid[1] = tmp[1]        
        
        self.Debug_view()

    def ExtendWall(self, x, y):
        #伸ばすことができる方向(1マス先が通路で2マス先まで範囲内)
        #2マス先が壁で自分自身の場合、伸ばせない
        direction = []
        if self.maze[x][y-1] == environment.ROAD and self.IsExtendingWall(x, y-2) == 0:
            direction.append(environment.UP)
        if self.maze[x+1][y] == environment.ROAD and self.IsExtendingWall(x+2, y) == 0:
            direction.append(environment.RIGHT)
        if self.maze[x][y+1] == environment.ROAD and self.IsExtendingWall(x, y+2) == 0:
            direction.append(environment.DOWN)
        if self.maze[x-1][y] == environment.ROAD and self.IsExtendingWall(x-2, y) == 0:
            direction.append(environment.LEFT)
        #伸ばすことのできる方向があるなら拡張
        if len(direction) > 0:
            self.SetWall(x, y)
            #伸ばす先が通路の場合は拡張を続ける
            isRoad = False
            dirindex = random.randrange(len(direction))

            if direction[dirindex] == environment.UP:
                isRoad = (self.maze[x, y-2] == environment.ROAD)
                y = y-1
                self.SetWall(x, y)
                y = y-1
                self.SetWall(x, y)
            elif direction[dirindex] == environment.DOWN:
                isRoad = (self.maze[x, y+2] == environment.ROAD)
                y = y+1
                self.SetWall(x, y)
                y = y+1
                self.SetWall(x, y)
            elif direction[dirindex] == environment.RIGHT:
                isRoad = (self.maze[x+2, y] == environment.ROAD)
                x = x+1
                self.SetWall(x, y)
                x = x+1
                self.SetWall(x, y)
            elif direction[dirindex] == environment.LEFT:
                isRoad = (self.maze[x-2, y] == environment.ROAD)
                x = x-1
                self.SetWall(x, y)
                x = x-1
                self.SetWall(x, y)

            if isRoad == True:
                self.ExtendWall(x, y)

        else:
            #現在拡張中の壁にぶつかる場合、バックして再開
            before = self.wall_stack.pop()
            self.ExtendWall(before[0], before[1])

    def BreakWall(self):
        while(True):
            x = random.randrange(1, SIZE-1)
            y = random.randrange(1, SIZE-1)
            if self.maze[x][y] == environment.WALL:
                self.maze[x][y] = environment.ROAD
                break
    
    def GetGrid(self,_length = 0,_x = 0,_y = 0):
        if _length == 0:
            while(True):
                x = random.randrange(1, SIZE-1)
                y = random.randrange(1, SIZE-1)
                if x != _x and y != _y and self.maze[x][y] == environment.ROAD:
                    return y, x
        else:
            while(True):
                x = random.randrange(1, SIZE-1)
                y = random.randrange(1, SIZE-1)
                l = abs( (_x - x) * (_x - x) + (_y - y) * (_y - y) )
                if x != _x and y != _y and l >= _length and self.maze[x][y] == environment.ROAD:
                    return y, x

    def IsExtendingWall(self, x, y):
        #指定のマスが現在拡張中の壁ならば1,そうでなければ0を返す。
        for i in range(0, len(self.wall_stack)):
            if self.wall_stack[i][0] == x and self.wall_stack[i][1] == y:
                return 1
        return 0

    def SetWall(self, x, y):
        self.maze[x][y] = environment.WALL
        if x % 2 == 0 and y % 2 == 0:
            self.wall_stack.append([x, y])

    def Debug_view(self):
        logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)
        logging.info("start_grid:[%i,%i]", self.start_grid[0], self.start_grid[1])
        logging.info("goal_grid:[%i,%i]", self.goal_grid[0], self.goal_grid[1])
        maze_map = ""
        for y in range(0, SIZE+2):
            for x in range(0, SIZE+2):
                if self.maze[y][x] == environment.WALL:
                    maze_map += "■ "
                elif x == self.start_grid[0] and y == self.start_grid[1]:
                    maze_map += "\033[33mS\033[0m "
                elif x == self.goal_grid[0] and y == self.goal_grid[1]:
                    maze_map += "\033[34mG\033[0m "
                else:
                    maze_map += "□ "
            maze_map += "\n"
        logging.info("\n%s", maze_map)