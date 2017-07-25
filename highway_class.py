import pygame
import traceback
from collections import namedtuple
from constants import *
from helpers import *
from IRL.irlworld  import *
from highway_mixin import HighwayMixin

# not efficient 
from copy import deepcopy

from abstract_car import AbstractCar
"""
Implements the Highway World 2.0 environment

"""

class Highway(HighwayMixin, IRLworld):


    # state vector:  index corresponds to lane and lane_positino 
    # value = (car id, car_speed) at lane and lane_position given by index
    
    car_list = []
    reference_pts = []

    def add_reference_pt(self, tree):
        self.reference_pts.append(tree)
    
    def __init__(self, num_lanes=3, highway_len = 700, lane_width=76):

        self.num_lanes = num_lanes
        self.highway_len = highway_len

        self.lane_width = lane_width

        self.HEIGHT = self.highway_len
        self.WIDTH = self.num_lanes * self.lane_width



    def get_car_state_record_list(self):
        car_state_records = []
        for car in self.car_list:
            car_state = car.get_car_state_record()
            car_state_records.append(car_state)
        return car_state_records

    def get_highway_state_record(self):
        d = dict()

        d['num_lanes'] = self.num_lanes
        d['highway_len'] = self.highway_len
        d['HEIGHT'] = self.HEIGHT
        d['WIDTH'] = self.WIDTH

        d['car_list'] = self.get_car_state_record_list()
        d['odd_time'] = False

        # adding in from highway mixin
        d['lane_sep_color'] = self.lane_sep_color
        d['lane_color']     = self.lane_color
        
        d['lane_width'] = self.lane_width

        d['increment'] = self.increment
        d['max_increment'] = self.max_increment


        return d

    def get_highway_param(self):
        return (self.num_lanes, self.highway_len, self.lane_width)
    
    def get_highway_state(self):
        highway_state = []
        highway_state.append(self.highway_param())

        for car in highway.car_list:
            car_state = car.get_state() # 11-tuple
            highway_state.append(car_state)
        highway_time_series.append(highway_state)
    
    # returns (id, #steps away, speed) of closest car in specified lane & dir
    def get_closest_car(self, lane, lane_pos, dir):
        # if no such lane
        if not in_range(lane, 0, self.num_lanes - 1) or \
           not in_range(lane_pos, 0, self.highway_len - 1): 
            return (-1, -1, -1)

        min_num_steps_away = self.highway_len + 10 # impossible
        closest_car = None

        for car in self.car_list:
            num_steps_away = dir * (car.lane_pos - lane_pos)
            if car.lane == lane and num_steps_away >= 0:

                 if (num_steps_away < min_num_steps_away):
                    min_num_steps_away = num_steps_away
                    closest_car = car

            
        # no nearby cars in specified lane and dir
        if min_num_steps_away == self.highway_len + 10 : 
            return (-1, -1, -1)

        return (closest_car.id, min_num_steps_away, closest_car.speed)

    # returns (id, #steps away, speed) of the closest cars ahead/behind 
    # in current lane & neighboring left/right lanes.
    def get_closest_cars(self, lane, lane_pos):
        closest_cars = []

        closest_left_ahead =  self.get_closest_car(lane - 1, lane_pos, dir = 1)
        closest_left_behind = self.get_closest_car(lane - 1, lane_pos, dir = -1)

        closest_ahead =  self.get_closest_car(lane, lane_pos + 1, dir = 1)
        closest_behind = self.get_closest_car(lane, lane_pos - 1, dir = -1)

        closest_right_ahead = self.get_closest_car(lane + 1, lane_pos, dir = 1)
        closest_right_behind= self.get_closest_car(lane + 1, lane_pos, dir = -1)
        
        closest_cars.append(closest_left_ahead)
        closest_cars.append(closest_left_behind)

        closest_cars.append(closest_ahead)
        closest_cars.append(closest_behind)
        
        closest_cars.append(closest_right_ahead)
        closest_cars.append(closest_right_behind)

        return closest_cars


    # get positions of all cars, project n steps in future, step by step
    # check at each point for crash
    def crash_in_n_steps(self, n):

        # initial positions
        future_positions = []
        for car in self.car_list:
            future_positions.append(car.get_simulate_step_param())


        num_cars = len(future_positions)

        for time_step in range(1,n):
            for i in range(num_cars):
                curr_car_pos = future_positions[i]
                future_positions[i] = AbstractCar.simulate_step(curr_car_pos)

            is_collision = is_crash(future_positions)
            if is_collision:
                return True
        
        return False




    def add_car(self, car):
        self.car_list.append(car)

    def remove_car(self, car):
        try:
            self.car_list.remove(car)
        except:
            print("Car not in car list")

    def set_all_back(self, amt_back):

        for car in self.car_list:
            car.set_car_back(amt_back)

        for ref_pt in self.reference_pts:
            ref_pt.set_back(amt_back)
