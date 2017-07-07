import pygame
from constants import *

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
num_other_cars = 0

def start():
    # setup highway, agent car, simulator, and other cars.
    highway = Highway(num_lanes=num_lanes, highway_len=highway_len)
    
    agent_car = AgentCar(highway, lane_pos = 0)
    simulator = Simulator(agent_car)

    # set up other car(s)
    for _ in range(num_other_cars):
        other_car = OtherCar(highway)
    agent_car.init_start_state()

    print("Restart")
    return (highway, agent_car, simulator)


def main():
    DONE = False
    PAUSE = False
    RESTART = False

    screen.fill(GREEN)

    (highway, agent_car, simulator) = start()

    while not (DONE or RESTART):
        for event in pygame.event.get():
            DONE,PAUSE,RESTART = check_event(event,highway,agent_car,simulator,\
                                    DONE, PAUSE, RESTART);
        redraw_all(screen, highway)
    print("Simulation Over")

    if RESTART:
        main();            # restart the game

main()
