import pygame
from init import init_game

screen = init_game();

from random import randint


from class_car import OtherCar, AgentCar
from class_highway import Highway

from redraw_all import redraw_all
from game_events import check_event

# general tweakable parameters
num_lanes = 3
highway_len = 1100
num_other_cars = 4

highway = Highway(num_lanes=num_lanes, highway_len=highway_len, num_speeds = 4)

# setup up agent car
agent_car = AgentCar(highway, lane=0, lane_pos=0, speed = 1)

# set up other car(s)
for _ in range(num_other_cars):
    other_car = OtherCar(highway)
agent_car.set_start_state()


# Main Loop
DONE = False
while not DONE:
    for event in pygame.event.get():
            DONE = check_event(event, highway.car_list, agent_car, DONE);
    redraw_all(screen, highway, agent_car)
