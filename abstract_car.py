from abc import ABCMeta, abstractmethod
import itertools
import pygame
from constants import *
from random import randint
import numpy as np
import itertools

class AbstractCar(object):

    __metaclass__ = ABCMeta

    counter = itertools.count(1)
    
    """ Car image size width = 228, height = 128 """
    WIDTH = 114 #228
    HEIGHT = 64 #128
    
    highway = []

    min_speed = 0.1
    max_speed = 15

    data = "smaller_data"


    def is_collision(self, new_lane, new_lane_pos):
        my_idx = self.highway.pos_to_idx(new_lane, new_lane_pos)

        # my car would collide with cars within the behind-ahead index range
        behind_idx = self.highway.pos_to_idx(new_lane, \
                                            max(0, new_lane_pos - self.WIDTH))
        ahead_idx = self.highway.pos_to_idx(new_lane,  
                    min(self.highway.highway_len-1, new_lane_pos + self.WIDTH))

        no_crash = True
        curr_idx = behind_idx
        
        while (no_crash and curr_idx <= ahead_idx):
            neighbor = self.highway.idx_to_state(curr_idx)
            no_crash = (neighbor == (-1, -1)) or (neighbor[0] == self.id)
            curr_idx += 1

        return (not no_crash)

    def rand_lane(self): return randint(0, self.highway.num_lanes - 1)
    def rand_lane_pos(self): return randint(0, self.highway.highway_len - self.WIDTH - 1)
    def rand_speed(self): return randint(self.min_speed, self.max_speed)

    # speed is chosen from a normal distribution - Normal params depend on lane
    # left lane (lane = 0) fastest, right lane slower 
    def normal_speed(self):

        # left-most lane moves fast, right-most moves slow
        if   self.lane == 0:                          mu, sigma = 10, 0.2
        elif self.lane == self.highway.num_lanes - 1: mu, sigma = 6, 0.2
        else:                                         mu, sigma = 3, 0.2

        self.speed = np.random.normal(mu, sigma, 1)[0]
        # ensure positive speed (or within speed limit)
        while (self.speed <= 0.5):
            self.speed = np.random.normal(mu, sigma, 1)[0]
        print("Set speed to %1.1f" % self.speed)

    def set_speed(self, speed, normal=True):
        if speed != -1: self.speed = speed
        elif normal: self.normal_speed()
        else: self.rand_speed()

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
        self.id = next(self.counter)

        self.highway = highway
        
        self.place(lane, lane_pos)
        self.set_speed(speed, normal=True)
        self.pixel_pos()

        self.highway.car_list.append(self)
        self.highway.add_car(self.id, self.lane, self.lane_pos, self. speed)


        # # features = #steps to car ahead/behind, its speed and my car speed
        # # for each lane
        # self.num_features = self.highway.num_lanes * 4 + 1

    def __eq__(self, other):
        return self.id == other.id

    def is_legal_pos(self, lane, lane_pos):
        return in_range(lane_pos, 0, self.highway.highway_len - 1) and \
                in_range(lane, 0, self.highway.num_lanes - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)

    def pixel_pos(self):
        self.x = self.lane_pos
        self.y = 5 + self.lane * (self.highway.lane_height + 1)
        return (self.x,self.y)

    def draw(self, screen):
        return screen.blit(self.image_car, self.pixel_pos())

    def move(self):
        old_lane, old_lane_pos = self.lane, self.lane_pos
        new_lane, new_lane_pos = self.lane, int(round(self.lane_pos + self.speed))

        reached_end = new_lane_pos >= self.highway.highway_len

        if reached_end:
            try: self.highway.car_list.remove(self)
            except: print("why is the car not in the car list?")
            
            self.highway.remove_car(self.lane, self.lane_pos)
            print("removed car")
            
            return

        if not self.is_legal_pos(new_lane, new_lane_pos): return

        self.lane, self.lane_pos = new_lane, new_lane_pos
        self.pixel_pos() 

        self.highway.update_car(self.id, old_lane, old_lane_pos, \
            self.lane, self.lane_pos, self.speed)


    def change_lane(self, dir):
        old_lane, new_lane = self.lane, self.lane + dir
        
        if not self.is_legal_pos(new_lane, self.lane_pos): return
    
        self.lane = self.lane + dir

        self.pixel_pos()

        self.highway.update_car(self.id, old_lane, self.lane_pos, \
            self.lane, self.lane_pos, self.speed)
        
    def change_speed(self, speed_change):
        new_speed = self.speed + speed_change
        
        if not self.is_legal_speed(new_speed): return

        self.speed = new_speed
        

    # feature = list (id, #steps away, speed) for cars ahead/behind and 
    # left, current, right lanes. At end, agent's id, speed, lane, & lane pos.
    def get_feature(self):
        closest_cars = self.highway.get_closest_cars(self.lane, self.lane_pos)
        closest_cars.append(self.id)
        closest_cars.append(self.speed)
        closest_cars.append(self.lane)
        closest_cars.append(self.lane_pos)
        return closest_cars

    def __str__(self):
        feat = self.get_feature()

        feat_len    = len(feat)
        my_id       = feat[feat_len - 4]
        my_speed    = feat[feat_len - 3]
        my_lane     = feat[feat_len - 2]
        my_lane_pos = feat[feat_len - 1]

        res = ("Features of car id = %d: \n " % my_id)
        res += ("Speed = %1.1f. Lane: %d. Lane Pos: %d. \n" % \
            (my_speed, my_lane, my_lane_pos))

        lane_strs = ["LEFT", "LEFT", "CURR", "CURR", "RIGHT", "RIGHT"]
        dir_strs = ["AHEAD", "BEHIND"]

        for i in range(0, feat_len - 4, 1):
            lane_str = lane_strs[i % 6]
            dir_str = dir_strs[i % 2]

            res += ("%6s and %6s: (id = %3d, steps away = %3d, speed = %2.1f) \n" % \
                (lane_str, dir_str, feat[i][0], feat[i][1], feat[i][2]))


        return res

    def print_feature(self, feat):

        feat_len    = len(feat)
        my_id       = feat[feat_len - 4]
        my_speed    = feat[feat_len - 3]
        my_lane     = feat[feat_len - 2]
        my_lane_pos = feat[feat_len - 1]

        print("Features of car id = %d: " % my_id)
        print("My speed = %1.1f. Lane: %d, Lane Pos: %d" % \
            (my_speed, my_lane, my_lane_pos))

        lane_strs = ["LEFT", "LEFT", "CURR", "CURR", "RIGHT", "RIGHT"]
        dir_strs = ["AHEAD", "BEHIND"]

        for i in range(0, feat_len - 4, 1):
            lane_str = lane_strs[i % 6]
            dir_str = dir_strs[i % 2]

            print("%6s and %6s: (id = %3d, steps away = %3d, speed = %2.1f)" % \
                (lane_str, dir_str, feat[i][0], feat[i][1], feat[i][2]))



