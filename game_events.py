""" Function which control game """
import pygame
from constants import *

CAR_MOVE_EVENT, t = pygame.USEREVENT+1, 50
pygame.time.set_timer(CAR_MOVE_EVENT, t)

# record highway every 0.5 seconds. 2 min traj => 240 len vector
RECORD_HIGHWAY_EVENT, s = pygame.USEREVENT+2, 500
pygame.time.set_timer(RECORD_HIGHWAY_EVENT, t)

# update acceleration
UPDATE_SIMULATOR, u = pygame.USEREVENT+2, 150
pygame.time.set_timer(UPDATE_SIMULATOR, u)

highway_time_series = []

def record_highway(highway):
    highway_state = []
    highway_state.append(highway.num_lanes)
    for car in highway.car_list:
        car_state = car.get_state() # 11-tuple
        highway_state.append(car_state)
    highway_time_series.append(highway_state)

def move_cars(car_list, agent_car):
    for car in car_list:
        if car != agent_car:
            car.move()
    DONE = agent_car.move()
    return DONE

def is_quit(event):
    return (event.type == pygame.QUIT) or \
        ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE))

def is_restart(event, PAUSE):
    return event.type == pygame.JOYBUTTONDOWN and event.button == R

def is_pause(event):
    return ((event.type == pygame.KEYDOWN and event.key == pygame.K_p) or \
        event.type == pygame.JOYBUTTONDOWN and event.button == P)

def is_blinker(event):
    return event.type == pygame.JOYBUTTONDOWN and \
        (event.button == LEFT_BLINKER or event.button == RIGHT_BLINKER)

def check_event(event, highway, agent_car, simulator, DONE, PAUSE, RESTART):
    if event.type == pygame.JOYBUTTONDOWN:
        print("button: ", event.button)
    
    # If user clicked close or quits
    if is_quit(event): 
        DONE = True
        return (DONE, PAUSE, RESTART, highway_time_series) 

    # check if resart
    if is_restart(event, PAUSE):
        RESTART = True
        return (DONE, PAUSE, RESTART, highway_time_series)
    
    # toggle pause
    if is_pause(event):
        PAUSE = not PAUSE

    if PAUSE:
        return (DONE, PAUSE, RESTART, None)

    if (event.type == CAR_MOVE_EVENT): 
        DONE = move_cars(highway.car_list, agent_car)

    if event.type == pygame.JOYAXISMOTION:
      simulator.set_axis(event.axis, event.value)

    if is_blinker(event):
        agent_car.toggle_blinker(event.button)

    if (event.type == RECORD_HIGHWAY_EVENT):
        record_highway(highway)

    # User pressed down on a key
    # if event.type == pygame.KEYDOWN:
        

    return (DONE, PAUSE, RESTART, highway_time_series)

# if event.key == pygame.K_LEFT: agent_car.change_lane(LEFT)
# if event.key == pygame.K_RIGHT: agent_car.change_lane(RIGHT)
# if event.key == pygame.K_UP: agent_car.change_speed(FASTER)
# if event.key == pygame.K_DOWN: agent_car.change_speed(SLOWER)
