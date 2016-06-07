#!/usr/bin/python

# Copyright (C) 2010 Michael Spang. You may redistribute this file
# under the terms of the FreeBSD license.

# CSE 190 Final Project
# Ethan Chan    A11221627   e1chan@ucsd.edu
# Richard Lin   A11365487   rgl001@ucsd.edu

"""Template for your tron bot"""

import tron
import random
import numpy as np
from sys import stderr

config = {
    'move_list': [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]
    ],
    'max_iterations': 100,
    'reward_pit': -10.0,
    'reward_goal': 10.0,
    'reward_step': -0.05
}

dirs = {
    'forward':  lambda (dx, dy): ( dx,  dy),
    'backward': lambda (dx, dy): (-dx, -dy),
    'left':     lambda (dx, dy): (-dy,  dx),
    'right':    lambda (dx, dy): ( dy, -dx),
}

types = {
    tron.FLOOR: 'FLOOR',
    tron.WALL:  'WALL',
    tron.ME:    'ME',
    tron.THEM:  'THEM'
}

class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return '\n'.join(
            ''.join(r) for r in
            np.vectorize(
                lambda n: n.policy or n.type
            )(self.nodes)
        )

    def __iter__(self):
        return self.nodes


class Node(object):
    def __init__(self, type, x, y):
        self.type = type
        self.policy = None
        self.x = x
        self.y = y
        self.neighbors = {}
        self.value = 0

    def __repr__(self):
        return '{}({}, {}) @ ({}, {})'.format(
            types[self.type], self.policy, self.value, self.x, self.y)

    def add_neighbor(self, direction, neighbor):
        self.neighbors[direction] = neighbor


def build_graph(board, nodes):

    for node in nodes.flat:

        if node.type == tron.WALL:
            continue

        for dx, dy in config['move_list']:
            x = node.x + dx
            y = node.y + dy

            if 0 <= x < board.width and 0 <= y < board.height:
                neighbor = nodes[x, y]
                node.add_neighbor((dx, dy), neighbor)

    return Graph(nodes)


def which_move(board):

    nodes = np.array([[
        Node(t, x, y)
        for x, t in enumerate(r)]
        for y, r in enumerate(board.board)])

    graph = build_graph(board, nodes)

    print >>stderr, "GRAPH: <<\n", graph, "\n>>"

    for src in graph.nodes.flat:
        print >>stderr, "node:", types[src.type], ", neigh:", src.neighbors


    # fill in your code here. it must return one of the following directions:
    #   tron.NORTH, tron.EAST, tron.SOUTH, tron.WEST

    # For now, choose a legal move randomly.
    # Note that board.moves will produce [NORTH] if there are no
    # legal moves available.
    return random.choice(board.moves())

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
