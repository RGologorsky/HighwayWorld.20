import pygame
""" Define constants """


# Set the width and height of the screen
screen_width = 1300
screen_height = 500

# colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0,   0,   255)
GRAY = (211,211,211)

# game events
LEFT = -1; RIGHT = 1
FASTER = 1; SLOWER = -1

# actions: left, right, slower, faster, zero change
Z = 0
L = 1; R = 2
S = -1; F = -2

# useful functions
def in_range(x, a, b):
    return a <= x and x <= b
