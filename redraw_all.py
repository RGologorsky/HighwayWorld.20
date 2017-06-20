import pygame
from constants import *
from init import init_game
from class_highway import Highway
from class_car import OtherCar

def redraw_all(screen, highway):
    screen.fill(GREEN)
    highway.draw(screen)
    pygame.display.flip()
