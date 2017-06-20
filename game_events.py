""" Function which control game """
import pygame
from constants import *

CAR_MOVE_EVENT, t = pygame.USEREVENT+1, 250
pygame.time.set_timer(CAR_MOVE_EVENT, t)

def move_cars(car_list, agent_car):
    for car in car_list:
        car.move()
    DONE = agent_car.move()
    return DONE

def check_event(event, car_list, agent_car, DONE):

    # If user clicked close
    if (event.type == pygame.QUIT) or \
        ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)): 
        DONE = True  # Flag that we are done so we exit this loop

    if (event.type == CAR_MOVE_EVENT):
        DONE = move_cars(car_list, agent_car)
    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
        # Figure out if it was an arrow key. If so
        # adjust speed.
        if event.key == pygame.K_LEFT:
            agent_car.change_lane(LEFT)
        if event.key == pygame.K_RIGHT:
             agent_car.change_lane(RIGHT)
        if event.key == pygame.K_UP:
            agent_car.change_speed(FASTER)
        if event.key == pygame.K_DOWN:
            agent_car.change_speed(SLOWER)

    # User let up on a key
    # if event.type == pygame.KEYUP:
    #     # If it is an arrow key, reset vector back to zero
    #     if event.key == pygame.K_LEFT:
    #         pass
    #     if event.key == pygame.K_RIGHT:
    #        pass
    #     if event.key == pygame.K_UP:
    #         y_speed = 0
    #     if event.key == pygame.K_DOWN:
    #         y_speed = 0
    return DONE
