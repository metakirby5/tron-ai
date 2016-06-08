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
    'max_iterations': 200,
    'discount_factor': 0.99,
    'reward_pit': -10.0,
    'reward_goal': 10.0,
    'reward_step': -0.05
}

to_str = {
    tron.FLOOR: 'FLOOR',
    tron.WALL:  'WALL',
    tron.ME:    'ME',
    tron.THEM:  'THEM',
    tron.EAST:  '>',
    tron.WEST:  '<',
    tron.SOUTH: 'v',
    tron.NORTH: '^'
}

rewards = {
    tron.FLOOR: config['reward_step'],
    tron.WALL:  config['reward_pit'],
    tron.ME:    config['reward_step'],
    tron.THEM:  config['reward_goal']
}

policies = {
    ( 0,  1):  tron.EAST,
    ( 0, -1):  tron.WEST,
    ( 1,  0):  tron.SOUTH,
    (-1,  0):  tron.NORTH,
}

class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return '\n'.join(
            ''.join(r) for r in
            np.vectorize(
                lambda n: to_str.get(n.policy, None) or n.kind
                #lambda n: str(n.value)[0:5] + '\t'
            )(self.nodes)
        )

    def __iter__(self):
        return self.nodes


class Node(object):
    def __init__(self, kind, x, y):
        self.kind = kind
        self.policy = None
        self.x = x
        self.y = y
        self.neighbors = {}
        self.value = 0

    def __repr__(self):
        return '{}({}, {}) @ ({}, {})'.format(
            to_str[self.kind], self.policy, self.value, self.x, self.y)

    def add_neighbor(self, direction, neighbor):
        self.neighbors[direction] = neighbor


def build_graph(board, nodes):

    for node in nodes.flat:

        if node.kind == tron.WALL:
            node.value = config['reward_pit']
            continue

        for dx, dy in config['move_list']:
            x = node.x + dx
            y = node.y + dy

            if 0 <= x < board.width and 0 <= y < board.height:
                neighbor = nodes[y, x]
                node.add_neighbor((dy, dx), neighbor)

    return Graph(nodes)

def which_move(board):

    nodes = np.array([[
        Node(t, x, y)
        for x, t in enumerate(r)]
        for y, r in enumerate(board.board)])

    graph = build_graph(board, nodes)

    # Map has updated, so recalculate optimal policy
    for i in xrange(config['max_iterations']):

        # For every node, calculate policies and values
        for src in graph.nodes.flat:

            # Find the best policy and value out of all actions
            policy = None
            best = src.value
            for a in src.neighbors:

                # Get the value of taking this action (assume certain movement)
                dest = src.neighbors[a]
                reward = rewards[dest.kind]
                value = (reward + config['discount_factor'] * dest.value)

                # Update if we have a better expected value
                if policy is None or value > best:
                    policy = a
                    best = value

            src.policy = policies.get(policy, policy)
            src.value = best

    for d, n in graph.nodes[board.me()].neighbors.iteritems():
        print >>stderr, "\tdir=", d, ", val=", n.value, n.kind

    move = graph.nodes[board.me()].policy
    print >>stderr, "GRAPH: <<\n", graph, "\n>>"
    print >>stderr, "moving:", to_str[move]
    return move

    # fill in your code here. it must return one of the following directions:
    #   tron.NORTH, tron.EAST, tron.SOUTH, tron.WEST

    # For now, choose a legal move randomly.
    # Note that board.moves will produce [NORTH] if there are no
    # legal moves available.
    # return random.choice(board.moves())

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
