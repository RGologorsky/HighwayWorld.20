from abc import ABCMeta, abstractmethod
import itertools
import pygame
from constants import *
from random import randint

def in_range(x, a, b):
    return a <= x and x <= b

class AbstractCar(object):

    __metaclass__ = ABCMeta

    counter = 0
    
    """ Car image size width = 228, height = 128 """
    WIDTH = 228
    HEIGHT = 128
    
    highway = []

    min_speed = 1
    max_speed = 4


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


        self.speed = speed if speed != -1 else self.rand_speed()
        self.place(lane, lane_pos)
        self.pixel_pos()

        # features = #steps to car ahead/behind, it's speed and my car speed
        # for each lane
        self.num_features = self.highway.num_lanes * 4 + 1

    def __eq__(self, other):
        return self.id == other.id

    def is_legal_pos(self, lane, lane_pos):
        return in_range(lane_pos, 0, self.highway.highway_len) and \
                in_range(lane, 0, self.highway.num_lanes )

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)

    def pixel_pos(self):
        self.x = self.lane_pos * self.highway.lane_unit_length
        self.y = 10 + self.lane * self.highway.lane_height
        return (self.x,self.y)

    def draw(self, screen):
        return screen.blit(self.image_car, self.pixel_pos())

    def move(self):
        old_lane, old_lane_pos = self.lane, self.lane_pos
        new_lane, new_lane_pos = self.lane, self.lane_pos + self.speed

        reached_end = new_lane_pos >= self.highway.highway_len

        if reached_end:
            self.highway.car_list.remove(self)
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
        old_lane, old_lane_pos = self.lane, self.lane_pos
        new_lane, new_lane_pos = self.lane + dir, self.lane_pos + self.speed
        
        if not self.is_legal_pos(new_lane, new_lane_pos):
            return
    
        self.lane = self.lane + dir
        self.lane_pos = self.lane_pos + self.speed

        self.pixel_pos()

        self.highway.update_car(self.id, old_lane, old_lane_pos, \
            self.lane, self.lane_pos, self.speed)
        
    def change_speed(self, speed_change):
        old_lane, old_lane_pos = self.lane, self.lane_pos
        new_speed = self.speed + speed_change
        
        if not self.is_legal_speed(new_speed):
            return

        self.speed = new_speed
        self.highway.update_car(self.id, old_lane, old_lane_pos, \
            self.lane, self.lane_pos, self.speed)

    # feature = list of [#steps ahead, ahead_car speed,
    # #steps behind, behind_car speed] for each lane
    # with the agent's car current speed at end
    def get_feature(self):
        closest_cars = self.highway.get_closest_cars(self.lane, self.lane_pos)
        closest_cars.append(self.speed)
        return closest_cars


    def print(self):
        feat = self.get_feature()

        print("Feautures of car id = %d: " % (self.id))
        print("My speed is: %d. Lane Pos: %d" % (self.speed, self.lane_pos))

        for lane in range(self.highway.num_lanes):
            idx = lane * 4
            print("Lane %d: %d steps ahead, speed %d. %d steps behind, speed = %d" % \
                (lane, feat[idx], feat[idx+1], feat[idx+2], feat[idx+3]))



