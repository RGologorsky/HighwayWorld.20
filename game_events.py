""" Function which control game """
import pygame
from constants import *
from helpers import *

from playback import *

highway_time_series = []

def record_highway(highway):
    highway_time_series.append(highway.get_highway_state_record())


def move_cars(car_list, agent_car):
    for car in car_list:
        if car != agent_car:
            car.move()
    DONE = agent_car.move()
    return DONE

def check_event(event, highway, agent_car, simulator, DONE, PAUSE, RESTART):
    if event.type == pygame.JOYBUTTONDOWN:
        print("button: ", event.button)

    if is_pause_pressed(event):
        PAUSE = not PAUSE

    if PAUSE:
        return (DONE, PAUSE, RESTART, None)
    
    # move cars, update positions
    if (event.type == CAR_MOVE_EVENT): 
        DONE = move_cars(highway.car_list, agent_car)

    # steering input
    if event.type == pygame.JOYAXISMOTION:
      simulator.set_axis(event.axis, event.value)

    # record highway
    if (event.type == RECORD_HIGHWAY_EVENT):
        record_highway(highway)

    # blinker input    
    if is_blinker(event):
        agent_car.toggle_blinker(event.button)


    # If user clicked close or quits
    if is_quit(event): 
        DONE = True

    if is_restart(event, PAUSE):
        RESTART = True
    
        
    if DONE or RESTART:
        Playback.write_recorded_data(highway_time_series)


    return (DONE, PAUSE, RESTART)

# if event.key == pygame.K_LEFT: agent_car.change_lane(LEFT)
# if event.key == pygame.K_RIGHT: agent_car.change_lane(RIGHT)
# if event.key == pygame.K_UP: agent_car.change_speed(FASTER)
# if event.key == pygame.K_DOWN: agent_car.change_speed(SLOWER)
