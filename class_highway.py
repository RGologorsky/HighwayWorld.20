import pygame
from constants import *
import numpy as np
from irlworld import *
from drawing_helpers import *
import traceback
"""
Implements the Highway World 2.0 environment

"""

class Highway(IRLworld):


    # state vector:  index corresponds to lane and lane_positino 
    # value = (car id, car_speed) at lane and lane_position given by index
    
    lane_sep_color = WHITE
    lane_color = GRAY
    
    lane_height = 75 # little more than Car.height

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
        self.state[idx] = (id, speed)

    def set_state_from_pos(self, lane, lane_pos, id, speed):
        idx = self.pos_to_idx(lane, lane_pos)
        self.set_state_from_idx(idx, id, speed)

    def __str__(self):
        res = "Highway State. \n"
        for idx in range(self.num_states):
            state = self.idx_to_state(idx)
            if state != (-1, -1):
                lane, lane_pos = self.idx_to_pos(idx)
                res += ("Lane = %d. Pos = %3d. Speed = %2.1f. ID = %2d. \n" % \
                    (lane, lane_pos, state[1], state[0]))
        return res

    def print_state(self):
        return print(str(self))


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
        self.set_state_from_pos(car_lane, car_lane_pos, car_id, curr_speed)

    def remove_car(self, car_lane, car_lane_pos):
        state_index = self.pos_to_idx(car_lane, car_lane_pos)
        self.state[state_index] = (-1, -1)

    def update_car(self, car_id, old_lane, old_lane_pos, new_lane, new_lane_pos, curr_speed):
        self.remove_car(old_lane, old_lane_pos)
        self.add_car(car_id, new_lane, new_lane_pos, curr_speed)

    # DRAWING FUNCTIONS

    def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, [x,y,self.highway_len,self.lane_height], 0)

    def draw_sep(self, screen, x, y):
        pygame.draw.line(screen, self.lane_sep_color, (x,y), (x + self.highway_len, y), 1)


    def draw_highway_state(self, screen, x, y):
        render_multi_line(screen, str(self), x, y)

    def draw_agent_car(self, agent_car, screen, x, y):
        render_multi_line(screen, str(agent_car), x, y)
        
    def draw(self, screen):
        # start at top-left
        x = 0
        curr_y = 0
        agent_car = None
        
        # draw lanes
        for i in range(self.num_lanes):
            
            self.draw_lane(screen, x, curr_y)
            curr_y += self.lane_height
            
            self.draw_sep(screen, x, curr_y)
            curr_y += 1

        # draw cars
        for car in self.car_list:
            car.draw(screen);    
            
            if (car.id == 1): 
                agent_car = car  

        # draw highway state
        x, curr_y  = x + 10, curr_y + 10
        self.draw_highway_state(screen, x, curr_y) 

        # draw agent car features
        if agent_car:
            x = screen_width - 500
            self.draw_agent_car(agent_car, screen, x, curr_y) 
