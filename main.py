import pygame
from init import init_game

screen = init_game();

from random import randint


from class_car import OtherCar, AgentCar
from class_highway import Highway
from class_simulator import Simulator

from redraw_all import redraw_all
from game_events import check_event

# general tweakable parameters
num_lanes = 3
highway_len = 700
num_other_cars = 6

highway = Highway(num_lanes=num_lanes, highway_len=highway_len)

# setup up agent car
agent_car = AgentCar(highway, lane_pos = 0)

# set up simulator
simulator = Simulator(agent_car)

# set up other car(s)
for _ in range(num_other_cars):
    other_car = OtherCar(highway)
agent_car.init_start_state()

# set up simulator
simulator = Simulator(agent_car)

# Main Loop
DONE = False
PAUSE = False
while not DONE:
    for event in pygame.event.get():
        DONE, PAUSE = \
            check_event(event, highway, agent_car, simulator, DONE, PAUSE);
    redraw_all(screen, highway)
print("Simulation Over")
