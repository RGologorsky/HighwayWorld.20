from abc import ABCMeta, abstractmethod
import itertools
import pygame
from constants import *
from random import randint
import numpy as np
import itertools
from math import cos, sin, radians

class AbstractCar(object):

    __metaclass__ = ABCMeta

    counter = itertools.count(1)
    
    """ Car image size width = 228, height = 128 """
    WIDTH = 104 #228
    HEIGHT = 48 #128
    
    highway = []

    min_speed = 0.1
    max_speed = 20

    data = "smaller_data_transparent_cropped"

    # general useful functions
    def center_to_upper_left(x, y):
        return (x - AbstractCar.WIDTH/2, y - AbstractCar.HEIGHT/2)

    def rand_lane(self): 
        return randint(0, self.highway.num_lanes - 1)
    
    def rand_lane_pos(self): 
        return randint(0, self.highway.highway_len - self.WIDTH - 1)
    
    def rand_speed(self): 
        return randint(self.min_speed, self.max_speed)

    def is_legal_lane(self, lane):
        return in_range(lane, 0, self.highway.num_lanes - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)

    def get_pixel_pos(self):
        return (self.x, self.y)

    def pixel_to_lane_pos(self, x, y):
        lane     = int(y / self.highway.lane_height)
        lane_pos = int(round(x))

        return (lane, lane_pos)

    # straight collision
    def is_collision(self, new_lane, new_lane_pos):
        behind_pos = max(0,new_lane_pos - self.WIDTH)
        ahead_pos =  min(new_lane_pos + self.WIDTH, self.highway.highway_len-1)

        my_idx      = self.highway.pos_to_idx(new_lane, new_lane_pos)
        behind_idx  = self.highway.pos_to_idx(new_lane, behind_pos)
        ahead_idx   = self.highway.pos_to_idx(new_lane, ahead_pos)

        no_crash = True
        curr_idx = behind_idx
        
        while (no_crash and curr_idx <= ahead_idx):
            neighbor = self.highway.idx_to_state(curr_idx)
            no_crash = (neighbor == (-1, -1)) or (neighbor[0] == self.id)
            curr_idx += 1

            if not no_crash:
                print("crash car idx %d" % (curr_idx - 1))

        if (not no_crash):
            print ("collision occured, car id %d" % self.id)
        return (not no_crash)

    # init functions
    def init_pixel_pos(self):
        self.x = self.lane_pos
        self.y = (self.lane + 0.5) * self.highway.lane_height

    def normal_speed(self):
        sigma = 1;

        if   self.lane == 0:                          mu = 5
        elif self.lane == self.highway.num_lanes - 1: mu = 4
        else:                                         mu = 3

        self.speed = np.random.normal(mu, sigma, 1)[0]

        while (self.speed <= 0.5):
            self.speed = np.random.normal(mu, sigma, 1)[0]
        print("Set speed to %1.1f" % self.speed)
    
    def init_speed(self, speed, normal=True):
        if speed != -1: 
            self.speed = speed
        elif normal:    
            self.normal_speed()
        else:           
            self.rand_speed()

    def init_place(self, lane, lane_pos):
        lane     = lane     if     lane != -1 else self.rand_lane()
        lane_pos = lane_pos if lane_pos != -1 else self.rand_lane_pos()

        while (self.is_collision(lane, lane_pos)):
            lane     = self.rand_lane()
            lane_pos = self.rand_lane_pos()

        self.lane     = lane
        self.lane_pos = lane_pos
    
    # update functions
    def update_pos(self, allow_collision = False):
        angle = radians(self.angle)
        new_x = self.x + self.speed * cos(angle)
        new_y = self.y - self.speed * sin(angle)

        new_lane, new_lane_pos = self.pixel_to_lane_pos(new_x, new_y)

        if self.is_legal_lane(new_lane): 
            yes_collision = self.is_collision(new_lane, new_lane_pos)
            
            if allow_collision or not yes_collision:
                self.highway.update_car(self.id, self.lane, self.lane_pos, \
                                    new_lane, new_lane_pos, self.speed)
                self.x, self.y           = new_x, new_y
                self.lane, self.lane_pos = new_lane, new_lane_pos

                return yes_collision
        return False

    def update_speed(self):
        alpha = 0.2

        new_speed = self.speed + 2 * self.acceleration - 3 * self.brake

        # acceleration friction
        if self.acceleration != 0:
            new_speed -= alpha * self.speed

        if self.is_legal_speed(new_speed): 
            self.speed = new_speed

        self.highway.update_car(self.id, self.lane, self.lane_pos, \
                                    self.lane, self.lane_pos, self.speed)

    def __eq__(self, other):
        return self.id == other.id
   
    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        self.id           = next(self.counter)
        self.highway      = highway
        self.acceleration = 0
        self.brake        = 0
        self.angle        = 0

        self.init_place(lane, lane_pos)
        self.init_speed(speed, normal=True)
        self.init_pixel_pos()

        self.highway.car_list.append(self)
        self.highway.add_car(self.id, self.lane, self.lane_pos, self.speed)

        print(self.highway)
        # # features = #steps to car ahead/behind, its speed and my car speed
        # # for each lane
        # self.num_features = self.highway.num_lanes * 4 + 1

    # rotate car image around center
    def rotate(self):
        self.image_car = pygame.transform.rotate(self.original_image, self.angle)
        rect = self.image_car.get_rect()
        rect.center = (self.x, self.y)  
        

    def draw(self, screen):
        (center_x, center_y) = self.get_pixel_pos()
        upper_left_pos = AbstractCar.center_to_upper_left(center_x, center_y)
        return screen.blit(self.image_car, upper_left_pos)

    def move(self, allow_collision = False):
        reached_end = self.lane_pos >= self.highway.highway_len - 1

        if reached_end:
            try: 
                self.highway.car_list.remove(self)
            except: 
                print("why is the car not in the car list?")
            
            self.highway.remove_car(self.lane, self.lane_pos)
            print("removed car")
            
            return

        self.rotate()
        self.update_speed()
        collision = self.update_pos(allow_collision)
        return collision

    def change_lane(self, dir):
        new_lane = self.lane + dir
        
        if self.is_legal_lane(new_lane):
            self.highway.update_car(self.id, self.lane, self.lane_pos, \
                                    new_lane, self.lane_pos, self.speed)

            self.lane = new_lane
            self.y    += dir * self.highway.lane_height
        
    def change_speed(self, speed_change):
        new_speed = self.speed + speed_change
        
        if self.is_legal_speed(new_speed): 
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



