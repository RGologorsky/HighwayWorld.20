from abc import ABCMeta, abstractmethod
import itertools
import pygame
from constants import *
from random import randint
import numpy as np

def in_range(x, a, b):
    return a <= x and x <= b

class AbstractCar(object):

    __metaclass__ = ABCMeta

    counter = 0
    
    """ Car image size width = 228, height = 128 """
    WIDTH = 114 #228
    HEIGHT = 64 #128
    
    highway = []

    min_speed = 1
    max_speed = 4

    data = "smaller_data"


    def is_collision(self, new_lane, new_lane_pos):
        my_idx = self.highway.get_state_index(new_lane, new_lane_pos)
        behind_idx = self.highway.get_state_index(new_lane, 
            max(0, new_lane_pos - self.WIDTH))
        ahead_idx = self.highway.get_state_index(new_lane, 
            min(self.highway.highway_len-1, new_lane_pos + self.WIDTH))

        # print("My, behind, ahead")
        # print(my_idx, behind_idx, ahead_idx)

        no_cars = True
        curr_idx = behind_idx
        
        while (no_cars and curr_idx <= ahead_idx):
            neighbor = self.highway.state[curr_idx] # = -1 or (id, car speed)
            no_cars = (neighbor == -1) or (neighbor[0] == self.id)
            curr_idx += 1

        return (not no_cars)

    def rand_lane(self):
        return randint(0, self.highway.num_lanes - 1)

    def rand_lane_pos(self):
        return randint(0, self.highway.highway_len - self.WIDTH - 1)

    def rand_speed(self):
        return randint(self.min_speed, self.max_speed)

    # speed is chosen from a normal distribution - Normal params depend on lane
    # left lane (lane = 0) fastest, right lane slower 
    def normal_speed(self):

        # left-most lane moves fast
        if self.lane == 0: 
            mu, sigma = 3, 0.3

        # right-most lane moves slow
        elif self.lane == self.highway.num_lanes - 1:
            mu, sigma = 1, 0.3

        # middle lanes move temperate speed
        else:
            mu, sigma = 2, 0.3

        self.speed = np.random.normal(mu, sigma, 1)[0]

    def set_speed(self, speed, normal=True):
        if speed != -1:
            self.speed = speed
            return
        
        if normal:
            self.normal_speed()
        else:
            self.rand_speed()

        return


    def place(self, lane, lane_pos):
        lane = lane if lane != -1 else self.rand_lane()
        lane_pos = lane_pos if lane_pos != -1 else self.rand_lane_pos()

        while (self.is_collision(lane, lane_pos)):
            lane = self.rand_lane()
            lane_pos = self.rand_lane_pos()

        self.lane = lane
        self.lane_pos = lane_pos


    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        self.highway = highway

        self.id = AbstractCar.counter
        AbstractCar.counter += 1


        self.place(lane, lane_pos)

        # if random, Normal speed distribution depends on lane.
        self.set_speed(speed, normal=True)

        self.pixel_pos()

        # features = #steps to car ahead/behind, it's speed and my car speed
        # for each lane
        self.num_features = self.highway.num_lanes * 4 + 1

        self.highway.car_list.append(self)
        self.highway.add_car(self.id, self.lane, self.lane_pos, self. speed)


    def __eq__(self, other):
        return self.id == other.id

    def is_legal_pos(self, lane, lane_pos):
        return in_range(lane_pos, 0, self.highway.highway_len - 1) and \
                in_range(lane, 0, self.highway.num_lanes - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)

    def pixel_pos(self):
        self.x = self.lane_pos * self.highway.lane_unit_length
        self.y = 5 + self.lane * (self.highway.lane_height + 1)
        return (self.x,self.y)

    def draw(self, screen):
        return screen.blit(self.image_car, self.pixel_pos())

    def move(self):
        old_lane, old_lane_pos = self.lane, self.lane_pos
        new_lane, new_lane_pos = self.lane, self.lane_pos + self.speed

        reached_end = new_lane_pos >= self.highway.highway_len

        if reached_end:
            try:
                self.highway.car_list.remove(self)
            except:
                print("why is the car not in the car list?")
            self.highway.remove_car(self.lane, self.lane_pos)
            print("removed car")
            return

        if not self.is_legal_pos(new_lane, new_lane_pos):
            return

        self.lane, self.lane_pos = new_lane, new_lane_pos
        self.pixel_pos() 

        self.highway.update_car(self.id, old_lane, old_lane_pos, \
            self.lane, self.lane_pos, self.speed)


    def change_lane(self, dir):
        old_lane, new_lane = self.lane, self.lane + dir
        
        if not self.is_legal_pos(new_lane, self.lane_pos):
            return
    
        self.lane = self.lane + dir

        self.pixel_pos()

        self.highway.update_car(self.id, old_lane, self.lane_pos, \
            self.lane, self.lane_pos, self.speed)
        
    def change_speed(self, speed_change):
        new_speed = self.speed + speed_change
        
        if not self.is_legal_speed(new_speed):
            return

        self.speed = new_speed
        

    # feature = list of [#steps ahead, ahead_car speed,
    # #steps behind, behind_car speed] for each lane
    # with the agent's car current speed at end
    def get_feature(self):
        closest_cars = self.highway.get_closest_cars(self.lane, self.lane_pos)
        closest_cars.append(self.id)
        closest_cars.append(self.speed)
        closest_cars.append(self.lane)
        closest_cars.append(self.lane_pos)
        return closest_cars


    def print_feature(self, feat):

        feat_len = len(feat)
        my_id = feat[feat_len - 4]
        my_speed = feat[feat_len - 3]
        my_lane = feat[feat_len - 2]
        my_lane_pos = feat[feat_len - 1]

        print("Features of car id = %d: " % my_id)
        print("My speed is: %d. Lane: %d, Lane Pos: %d" % \
            (my_speed, my_lane, my_lane_pos))

        for lane in range(self.highway.num_lanes):
            idx = lane * self.highway.num_speeds
            print("Lane %d: %d steps ahead, speed %d. %d steps behind, speed = %d" % \
                (lane, feat[idx], feat[idx+1], feat[idx+2], feat[idx+3]))



