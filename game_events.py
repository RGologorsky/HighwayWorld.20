""" Function which control game """
import pygame
from constants import *

CAR_MOVE_EVENT, t = pygame.USEREVENT+1, 250
pygame.time.set_timer(CAR_MOVE_EVENT, t)

def move_cars(car_list, agent_car):
    for car in car_list:
        if car != agent_car:
            car.move()
    DONE = agent_car.move()
    return DONE

def check_event(event, car_list, agent_car, DONE, PAUSE):

    # If user clicked close or quits
    if (event.type == pygame.QUIT) or \
        ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
        DONE = True 

    # toggle pause
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
        PAUSE = not PAUSE

    if PAUSE: return (DONE, PAUSE)

    if (event.type == CAR_MOVE_EVENT): 
        DONE = move_cars(car_list, agent_car)

    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT: agent_car.change_lane(LEFT)
        if event.key == pygame.K_RIGHT: agent_car.change_lane(RIGHT)
        if event.key == pygame.K_UP: agent_car.change_speed(FASTER)
        if event.key == pygame.K_DOWN: agent_car.change_speed(SLOWER)

    return (DONE, PAUSE)
