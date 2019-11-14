""" Definitions of some Still Life configurations. """
import numpy as np


BLOCK = np.array([
    [1, 1],
    [1, 1],
])

BEEHIVE = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
])

LOAF = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
])

BOAT = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
])

TUB = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
])
