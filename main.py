import pygame
from random import randint

from constants import *


from car_class       import AgentCar, OtherCar
from highway_class   import Highway
from simulator_class import Simulator
from tree_class      import Tree
from game_events     import check_event

from helpers import *

# general tweakable parameters
num_lanes = 3
highway_len = 700
num_other_cars = 4


def init_screen():
    pygame.init()
    default_font = pygame.font.SysFont('Arial', 15)
    default_font.set_bold(True)
    screen = pygame.display.set_mode((screen_width,screen_height))
    print("<< Game started >>")
    return screen

screen = init_screen()

def start():
    # setup highway, agent car, simulator, and other cars.
    highway = Highway(num_lanes=num_lanes, highway_len=highway_len)
    highway.car_list = []

    # tree (reference point)
    tree = Tree(highway)
    highway.add_reference_pt(tree)

    mid_lane_pos = int(highway_len/2)
    
    agent_car = AgentCar(highway, lane_pos = mid_lane_pos)
    simulator = Simulator(agent_car)

    # set up other car(s)
    for _ in range(num_other_cars):
        other_car = OtherCar(highway)
    agent_car.init_start_state()


    draw_list = [highway, tree]

    print("Start")
    return (highway, agent_car, simulator, draw_list)

def main():
    DONE, PAUSE, RESTART = False, False, False
    
    screen.fill(GREEN)

    (highway, agent_car, simulator, draw_list) = start()

    while not (DONE or RESTART):
        for event in pygame.event.get():
            DONE,PAUSE,RESTART = check_event(event,highway,agent_car,simulator,\
                                    DONE, PAUSE, RESTART);
        redraw_all(screen, draw_list)
    print("Simulation Over")

    if RESTART:
        main();            # restart the game

main()
