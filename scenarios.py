import pygame
from random import randint, choice

from constants import *


from car_class       import *
from highway_class   import Highway
from simulator_class import Simulator
from tree_class      import Tree


def get_random_other_car(highway, simulator):
    other_cars = [OtherCar, SchoolBus, LongTruck, MediumTruck]
    ChosenCar = choice(other_cars)
    return ChosenCar(highway, simulator)


def init_scenario(scenario_num):
    if   scenario_num == 0: return init_scenario_0()
    elif scenario_num == 1: return init_scenario_1()
    else:                   return init_scenario_0()

def init_screen():
    pygame.init()
    default_font = pygame.font.SysFont('Arial', 15)
    default_font.set_bold(True)
    screen = pygame.display.set_mode((screen_width,screen_height))

    # set background
    # if is_image:
    #     bg = pygame.image.load("images/grass_background.png")
    # else:
    screen.fill(background_color)


    print("<< Game started >>")
    return screen

screen = init_screen()


def init_scenario_0():

    # general parameters
    num_lanes = 4
    highway_len = screen_height
    num_other_cars = 7

    return setup(num_lanes, highway_len, num_other_cars)

def init_scenario_1():

    # general parameters
    num_lanes = 5
    highway_len = screen_height
    num_other_cars = 10

    agent_car_file = "other_car"
    OtherCarType = None

    return setup(num_lanes, highway_len, num_other_cars, agent_car_file, OtherCarType)

def setup(num_lanes, highway_len, num_other_cars, agent_car_file="other_car", \
            OtherCarType = OtherCar, accel_max=0.5, degree_max=540):

    # setup highway, agent car, simulator, and other cars.
    highway = Highway(num_lanes=num_lanes, highway_len=highway_len)
    highway.car_list = []

    # tree (reference point)
    tree = Tree(highway.get_highway_param())
    highway.add_reference_pt(tree)

    agent_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    mid_lane_pos = int(highway_len/2)
    agent_car = AgentCar(highway, agent_simulator, lane=1, lane_pos = mid_lane_pos, file_name = agent_car_file)

    # set up other car(s)
    other_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    
    for _ in range(num_other_cars):
        if OtherCarType:
            other_car = OtherCarType(highway, other_car_simulator)
        else:
            other_car = get_random_other_car(highway, other_car_simulator)
    agent_car.init_start_state()


    draw_list = [highway, tree]

    print("Start")
    return (highway, agent_car, agent_simulator, draw_list, screen)

def init_scenario_0():

    # general parameters
    num_lanes = 2
    num_other_cars = 4
    highway_len = 700
    accel_max=0.5
    degree_max=540


    # setup highway, agent car, simulator, and other cars.
    highway = Highway(num_lanes=num_lanes, highway_len=highway_len)
    highway.car_list = []

    # tree (reference point)
    tree = Tree(highway.get_highway_param())
    highway.add_reference_pt(tree)

    agent_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    mid_lane_pos = int(highway_len/2)


    agent_car = AgentCar(highway, agent_simulator, lane=0, lane_pos = 3./10 * highway_len, speed=5)

    # set up other car(s)
    
    other_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    
    car_FA = OtherCar(highway, other_car_simulator, lane=0, lane_pos = 9./10 * highway_len, speed=4.5)
    car_RA = OtherCar(highway, other_car_simulator, lane=0, lane_pos = 1./10 * highway_len)

    car_FB = OtherCar(highway, other_car_simulator, lane=1, lane_pos = 9./10 * highway_len, speed = 3.5)

    merging_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    car_B = MergingCar(highway, agent_car, merging_car_simulator, lane=1, lane_pos = 2.5/10 * highway_len, speed = 3.5)


    draw_list = [highway, tree]

    print("Start")
    return (highway, agent_car, agent_simulator, draw_list, screen)

def init_scenario_2():

    # general parameters
    num_lanes = 2
    num_other_cars = 4
    highway_len = 700
    accel_max=0.5
    degree_max=540


    # setup highway, agent car, simulator, and other cars.
    highway = Highway(num_lanes=num_lanes, highway_len=highway_len)
    highway.car_list = []

    # tree (reference point)
    tree = Tree(highway.get_highway_param())
    highway.add_reference_pt(tree)

    agent_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    mid_lane_pos = int(highway_len/2)


    agent_car = AgentCar(highway, agent_simulator, lane=0, lane_pos = 3./10 * highway_len, speed=5)

    # set up other car(s)
    
    other_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    
    car_FA = OtherCar(highway, other_car_simulator, lane=0, lane_pos = 9./10 * highway_len, speed=4.5)
    car_RA = OtherCar(highway, other_car_simulator, lane=0, lane_pos = 1./10 * highway_len)

    car_FB = OtherCar(highway, other_car_simulator, lane=1, lane_pos = 9./10 * highway_len, speed = 3.5)

    merging_car_simulator = Simulator(accel_max = accel_max, degree_max = 540)
    car_B = MergingCar(highway, agent_car, merging_car_simulator, lane=1, lane_pos = 2.5/10 * highway_len, speed = 3.5)


    draw_list = [highway, tree]

    print("Start")
    return (highway, agent_car, agent_simulator, draw_list, screen)
