#!/usr/bin/python

# Copyright (C) 2010 Michael Spang. You may redistribute this file
# under the terms of the FreeBSD license.

"""Moves in a random direction"""

import random, tron

def which_move(board):
    return random.choice(board.moves())

# make a move each turn
for board in tron.Board.generate():
    tron.move(which_move(board))
