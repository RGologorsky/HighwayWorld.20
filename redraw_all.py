import pygame
from constants import *
from init import init_game
from class_highway import Highway
from class_car import OtherCar

def redraw_all(screen, highway, agent_car):
    screen.fill(WHITE)
    highway.draw(screen)
    agent_car.draw(screen)
    pygame.display.flip()
