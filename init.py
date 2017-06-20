""" Define what engine need """
import pygame
from constants import *

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    print("<< Game started >>")
    return screen
