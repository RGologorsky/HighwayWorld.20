""" Function which control game """
import pygame
from constants import *
from helpers import *
from math import radians
from playback import *

highway_param = None
highway_time_series = []

def record_highway(highway):
    highway_time_series.append(highway.get_highway_cars())

    global highway_param

    if not highway_param:
        highway_param = highway.get_highway_param()


def move_cars(car_list, agent_car):
    for car in car_list:
            DONE = car.move()
            if DONE:
                print("done by car: ", car.role)
                return DONE
    return False

def check_event(event, highway, agent_car, simulator, DONE, PAUSE, RESTART):
    
    if DONE or RESTART:
       return (DONE, PAUSE, RESTART)

    # If user clicked close or quits
    if is_quit(event): 
        DONE = True

    if is_restart(event, PAUSE):
        RESTART = True

    if event.type == pygame.JOYBUTTONDOWN:
        print("button: ", event.button)

    if is_pause_pressed(event):
        PAUSE = not PAUSE

    if PAUSE:
        return (DONE, PAUSE, RESTART)
    
    # move cars, update positions
    if (event.type == CAR_MOVE_EVENT): 
        DONE = move_cars(highway.car_list, agent_car)

    # steering input
    if event.type == pygame.JOYAXISMOTION:
      simulator.set_axis(event.axis, event.value)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:     
            agent_car.speed += 0.1
            # agent_car.simulator.u1 += 0.02
        if event.key == pygame.K_DOWN:
            agent_car.speed -= 0.1   
            # agent_car.simulator.u1 -= 0.02
        if event.key == pygame.K_LEFT:   agent_car.simulator.u2 += radians(1)
        if event.key == pygame.K_RIGHT:  agent_car.simulator.u2 -= radians(1)

    # record highway
    if (event.type == RECORD_HIGHWAY_EVENT):
        record_highway(highway)

    # blinker input    
    if is_blinker(event):
        agent_car.toggle_blinker(event.button)


    
        
    if DONE or RESTART:
        highway_data = (highway_param, highway_time_series)
        Playback.write_recorded_data(highway_data)


    return (DONE, PAUSE, RESTART)
