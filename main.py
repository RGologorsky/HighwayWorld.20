import pygame
from random import randint

from constants import *


from car_class       import AgentCar, OtherCar
from highway_class   import Highway
from simulator_class import Simulator
from tree_class      import Tree
from game_events     import check_event

from helpers import *

from playback import *

# general tweakable parameters
num_lanes = 4
highway_len = 700
num_other_cars = 6

accel_max = 0.5

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
    tree = Tree(highway.get_highway_param())
    highway.add_reference_pt(tree)

    agent_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    mid_lane_pos = int(highway_len/2)
    agent_car = AgentCar(highway, agent_simulator, lane=1, lane_pos = mid_lane_pos)

    # set up other car(s)
    other_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    for _ in range(num_other_cars):
        other_car = OtherCar(highway, other_car_simulator)
    agent_car.init_start_state()


    draw_list = [highway, tree]

    print("Start")
    return (highway, agent_car, agent_simulator, draw_list)

# returns when DONE
def play_game():
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
        play_game();            # restart the game

    return DONE

def playback():
    num = 1

    highway_time_series = Playback.get_recorded_data(num)
    
    print("highway time series")
    print(highway_time_series)

    num_time_steps = len(highway_time_series)
    curr_time_step = 0
    while curr_time_step != num_time_steps:
        for event in pygame.event.get():
            curr_time_step = check_playback_event(event, screen, \
                highway_time_series, curr_time_step);
    print("Playback Over")


def main():
    DONE = play_game()
    if DONE:
        playback()

main()
