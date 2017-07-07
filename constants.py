import pygame
""" Define constants """


# Set the width and height of the screen
screen_width = 900
screen_height = 700

# colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0,   0,   255)
GRAY = (211,211,211)
YELLOW = (255,255,0)

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

# simulator constants
SIMULATOR_NAME = "G920 Driving Force Racing Wheel for Xbox One"
STEERING_WHEEL_AXIS    = 0
ACCELERATOR_PEDAL_AXIS = 1 
BRAKE_PEDAL_AXIS       = 2
CLUTCH_PEDAL_AXIS      = 3

AXIS_NAMES = ["STEERING_WHEEL_AXIS", "ACCELERATOR_PEDAL_AXIS", \
              "BRAKE_PEDAL_AXIS", "CLUTCH_PEDAL_AXIS"]

# joystick buttons
A = 0
B = 1
X = 2
Y = 3
