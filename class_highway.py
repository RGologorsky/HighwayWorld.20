import pygame
from constants import *
import numpy as np
from irlworld import *
import traceback

from mixin_highway import HighwayMixin


"""
Implements the Highway World 2.0 environment

"""

class Highway(HighwayMixin, IRLworld):


    # state vector:  index corresponds to lane and lane_positino 
    # value = (car id, car_speed) at lane and lane_position given by index
    
    car_list = []
    
    def __init__(self,num_lanes=3, highway_len = 1100, 
                    max_num_cars=10, discount = 0.8):

        self.num_lanes = num_lanes
        self.highway_len = highway_len

        # for each position (lane, lane_pos), state = (car id, car speed)
        self.num_states = num_lanes * highway_len
        self.state = [(-1, -1)] * self.num_states


    def pos_to_idx(self, curr_lane, curr_lane_pos):
        return curr_lane * self.highway_len + curr_lane_pos

    def idx_to_pos(self, index):
        return (index/self.highway_len, index % self.highway_len)

    def idx_to_state(self, idx):
        if idx < 0 or idx >= self.num_states:
            print("Idx to State. Out of bounds index: %d" % idx)
            traceback.print_stack()
        return self.state[idx]

    def pos_to_state(self, lane, lane_pos):
        idx = self.pos_to_idx(lane, lane_pos)
        return self.idx_to_state(idx)

    def set_state_from_idx(self, idx, id, speed):
        try: 
            self.state[idx] = (id, speed)
        except:
            print("idx not in range: %d" % idx)
            pos = self.idx_to_pos(idx)
            print("pos: lane %d, lane pos %d" % pos)

    def set_state_from_pos(self, lane, lane_pos, id, speed):
        idx = self.pos_to_idx(lane, lane_pos)
        self.set_state_from_idx(idx, id, speed)


    # returns (id, #steps away, speed) of closest car in specified lane & dir
    def get_closest_car(self, lane, lane_pos, dir):
        # if no such lane
        if not in_range(lane, 0, self.num_lanes - 1) or \
           not in_range(lane_pos, 0, self.highway_len - 1): 
            return (-1, -1, -1)

        num_steps_away = 0
        near_state = (-1, -1)

        while (in_range(lane_pos+num_steps_away, 0, self.highway_len - 1) and \
                    near_state == (-1, -1)):
                
                near_state = self.pos_to_state(lane, lane_pos + num_steps_away)
                num_steps_away += dir
            
        # no nearby cars in specified lane and dir
        if near_state == (-1, -1): return (-1, -1, -1)
        return (near_state[0], abs(num_steps_away), near_state[1])


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


    def add_car(self, car_id, car_lane, car_lane_pos, curr_speed):
        car_lane_pos = min(self.highway_len - 1, car_lane_pos)
        
        self.set_state_from_pos(car_lane, car_lane_pos, car_id, curr_speed)

    def remove_car(self, car_lane, car_lane_pos):
        car_lane_pos = min(self.highway_len - 1, car_lane_pos)

        try:
            state_index = self.pos_to_idx(car_lane, car_lane_pos)
            self.state[state_index] = (-1, -1)
        except:
            print("index not in range: %d" % state_index)
            pos = self.idx_to_pos(state_index)
            print("pos: lane %d, lane pos %d" % pos)

    def update_car(self, car_id, old_lane, old_lane_pos, new_lane, new_lane_pos, curr_speed):
        self.remove_car(old_lane, old_lane_pos)
        self.add_car(car_id, new_lane, new_lane_pos, curr_speed)
