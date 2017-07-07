from abc import ABCMeta, abstractmethod
import itertools
import pygame
from constants import *
from random import randint
import numpy as np
import itertools
from math import cos, sin, radians
from mixin_abstract_car import AbstractCarMixin

class AbstractCar(AbstractCarMixin, object):

    __metaclass__ = ABCMeta

    # counter = itertools.count(1)
    
    min_speed = 0.1
    max_speed = 20
    
    # init functions

    # start cars in the middle of their lane
    def init_pixel_pos(self):
        self.y = self.highway.highway_len - self.lane_pos
        self.x = (self.lane + 0.5) * self.highway.lane_width

    # set speed sampled from a Normal distribution
    def normal_speed(self):
        sigma = 1;

        if   self.lane == 0:                          mu = 5
        elif self.lane == self.highway.num_lanes - 1: mu = 4
        else:                                         mu = 3

        self.speed = np.random.normal(mu, sigma, 1)[0]

        while (self.speed <= 0.5):
            self.speed = np.random.normal(mu, sigma, 1)[0]
        print("Set speed to %1.1f" % self.speed)
    
    # set initial speed
    def init_speed(self, speed, normal=True):
        if speed != -1: self.speed = speed
        elif normal:    self.normal_speed()
        else:           self.rand_speed()

    # set initial lane and lane position
    def init_place(self, lane, lane_pos):
        lane     = lane     if     lane != -1 else self.rand_lane()
        lane_pos = lane_pos if lane_pos != -1 else self.rand_lane_pos()

        while (self.is_collision(lane, lane_pos)):
            lane     = self.rand_lane()
            lane_pos = self.rand_lane_pos()

        self.lane     = lane
        self.lane_pos = lane_pos
    
    # update functions

    # update pos returns whether updated position caused collision
    def update_pos(self, allow_collision = False):
        angle = radians(self.angle)

        # self.heading += self.speed * angle

        # new_x = self.x + self.speed * cos(self.heading)
        # new_y = self.y - self.speed * sin(self.heading)
        
        new_x = self.x + self.speed * sin(angle)
        new_y = self.y - self.speed * cos(angle)

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
        friction = 0.2

        new_speed = self.speed

        if self.acceleration != 0:
            new_speed += 2* self.acceleration - friction*self.speed

        if self.brake != 0:
            new_speed -= 3* self.brake - friction*self.speed

        if self.is_legal_speed(new_speed): 
            self.speed = new_speed

        self.highway.update_car(self.id, self.lane, self.lane_pos, \
                                    self.lane, self.lane_pos, self.speed)
   
    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        counter = itertools.count(1)
        self.counter = counter
        self.id           = next(self.counter)
        self.highway      = highway
        self.acceleration = 0
        self.brake        = 0
        self.angle        = 0

        self.heading      = 0

        self.init_place(lane, lane_pos)
        self.init_speed(speed, normal=True)
        self.init_pixel_pos()

        self.highway.car_list.append(self)
        self.highway.add_car(self.id, self.lane, self.lane_pos, self.speed)

        # # features = #steps to car ahead/behind, its speed and my car speed
        # # for each lane
        # self.num_features = self.highway.num_lanes * 4 + 1
        

    def move(self, allow_collision = False):
        reached_end = self.lane_pos >= self.highway.highway_len - 1

        if reached_end:
            self.highway.remove_car(self.lane, self.lane_pos)
            print("Removed car from our highway state")

            try:    self.highway.car_list.remove(self)
            except: print("Failed to remove car from highway car list")
            
            
            return

        self.rotate()
        self.update_speed()
        collision = self.update_pos(allow_collision)
        return collision

    # Keyboard input or regulated speed change to car in front
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


