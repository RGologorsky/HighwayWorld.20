import pygame
""" Define constants """


# Set the width and height of the screen
screen_width = 1000
screen_height = 1000

# colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0,   0,   255)
GRAY = (211,211,211)
YELLOW = (255,255,0)

# # action
# LEFT = -1; RIGHT = 1
# FASTER = 1; SLOWER = -1

# actions: left, right, slower, faster, zero change
Z = 0
L = 1; R = 2
S = -1; F = -2


# simulator constants
SIMULATOR_NAME = "G920 Driving Force Racing Wheel for Xbox One"
STEERING_WHEEL_AXIS    = 0
ACCELERATOR_PEDAL_AXIS = 1 
BRAKE_PEDAL_AXIS       = 2
CLUTCH_PEDAL_AXIS      = 3

AXIS_NAMES = ["STEERING_WHEEL_AXIS", "ACCELERATOR_PEDAL_AXIS", \
              "BRAKE_PEDAL_AXIS", "CLUTCH_PEDAL_AXIS"]

# joystick buttons
# A = 0
# B = 1
# X = 2
# Y = 3

RIGHT_BLINKER = 1
LEFT_BLINKER  = 2

P = 6  # P = PAUSE
R = 10 # R = RESART

# MOVE EVENT FREQUENCY
CAR_MOVE_EVENT, t = pygame.USEREVENT+1, 25
pygame.time.set_timer(CAR_MOVE_EVENT, t)

# record highway every 0.10 seconds. 1 min traj => 600 len vector
RECORD_HIGHWAY_EVENT, s = pygame.USEREVENT+2, 100
pygame.time.set_timer(RECORD_HIGHWAY_EVENT, s)

# playback highway event every 0.5 seconds. 2 min traj => 240 len vector
PLAYBACK_HIGHWAY_EVENT = RECORD_HIGHWAY_EVENT
pygame.time.set_timer(PLAYBACK_HIGHWAY_EVENT, s)
