import pygame
from constants import *
import numpy as np

class Highway(object):

    # state vector:  index corresponds to lane and lane_positino 
    # value = (car id, car_speed) at lane and lane_position given by index
    
    lane_sep_color = WHITE
    lane_color = GRAY
    lane_height = 150 # little more than Car.height
    lane_unit_length = 1 # little more than Car.width

    car_list = []
    
    def __init__(self,num_lanes=3, highway_len = 1100, num_speeds = 4):

        self.num_lanes = num_lanes
        self.highway_len = highway_len
        self.lane_width = highway_len * self.lane_unit_length

        self.num_states = num_lanes*highway_len
        self.state = [-1] * self.num_states

    def get_state(self, min_index, max_index):
        return self.state[min_index, max_index]

    def get_state_index(self, curr_lane, curr_lane_pos):
        return curr_lane * self.highway_len + curr_lane_pos

    def deciper_index(self, index):
        return (index/self.highway_len, index % self.highway_len)

    def get_state_elem(self, lane, lane_pos):
        idx = self.get_state_index(lane, lane_pos)
        if idx < 0 or idx >= self.num_states:
            print("state elem, looking @ index %d" % idx)
            print("lane %d, lane_pos %d" % (lane, lane_pos))
        return self.state[idx]

    def print_state(self):
        print("Highway State")
        for i in range(self.num_states):
            elem = self.state[i]
            if elem != -1:
                lane, lane_pos = self.deciper_index(i)
                print("Car. ID = %d, Lane = %d, Lane Pos = %d" % \
                    (elem[0], lane, lane_pos))
        print("End State print")

    def get_closest_cars(self, curr_lane, curr_lane_pos):
        closest_cars = []
        for lane in range(self.num_lanes):
            
            num_steps_ahead = 0 if lane != curr_lane else 1
            num_steps_behind = 0 if lane != curr_lane else 1

            ahead_state_elem = \
                self.get_state_elem(lane, curr_lane_pos + num_steps_ahead)
            behind_state_elem = \
                self.get_state_elem(lane, curr_lane_pos - num_steps_behind)
            
            while (curr_lane_pos + num_steps_ahead < self.highway_len - 1 and \
                    ahead_state_elem == -1):

                num_steps_ahead += 1
                ahead_state_elem = \
                    self.get_state_elem(lane,curr_lane_pos+num_steps_ahead)
            
            while (curr_lane_pos - num_steps_behind > 0 and \
                behind_state_elem == -1):
    
                num_steps_behind += 1
                behind_state_elem = \
                    self.get_state_elem(lane,curr_lane_pos-num_steps_behind)

            # no car ahead
            if ahead_state_elem == -1:
                num_steps_ahead, ahead_car_speed = -1 
            
            else: 
                ahead_car_speed = ahead_state_elem[1]

            # no car behind
            if behind_state_elem == -1:
                num_steps_ahead, behind_car_speed = -1 
            
            else: 
                behind_car_speed = ahead_state_elem[1]
            

            closest_cars.append(num_steps_ahead)
            closest_cars.append(ahead_car_speed)

            closest_cars.append(num_steps_behind)
            closest_cars.append(behind_car_speed)

        return closest_cars


    def add_car(self, car_id, car_lane, car_lane_pos, curr_speed):
        state_index = self.get_state_index(car_lane, car_lane_pos)
        self.state[state_index] = (car_id, curr_speed)

    def remove_car(self, car_lane, car_lane_pos):
        state_index = self.get_state_index(car_lane, car_lane_pos)
        self.state[state_index] = -1

    def update_car(self, car_id, old_lane, old_lane_pos, new_lane, new_lane_pos, curr_speed):
        self.remove_car(old_lane, old_lane_pos)
        self.add_car(car_id, new_lane, new_lane_pos, curr_speed)

        # self.print_state()

    def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, [x,y,self.lane_width,self.lane_height], 0)

    def draw_sep(self, screen, x, y):
        pygame.draw.line(screen, self.lane_sep_color, (x,y), (x + self.lane_width, y), 1)


    def draw(self, screen):
        # start at top-left
        x = 0
        curr_y = 0
        
        # draw lanes
        for i in range(self.num_lanes):
            
            self.draw_lane(screen, x, curr_y)
            curr_y += self.lane_height
            
            self.draw_sep(screen, x, curr_y)
            curr_y += 1

        # draw cars
        for car in self.car_list:
            car.draw(screen);
