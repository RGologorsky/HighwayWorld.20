# Abstract Car Mixin
# general useful functions, constants

import pygame
import numpy as np
from random import randint
from math import pi, radians, degrees, cos, sin
from constants import *
from helpers import *


class AbstractCarMixin(object):
    
    WIDTH = 48 #228
    HEIGHT = 104 #128

    data = "rot_trans"

    # init functions
    def lane_center_to_pixel_pos(self, lane, lane_pos):
        x = (lane + 0.5) * self.highway.lane_width
        y = self.highway.highway_len - lane_pos
        return (x, y)

    # start cars in the middle of their lane
    def init_pixel_pos(self):
        self.x, self.y = self.lane_center_to_pixel_pos(self.lane, self.lane_pos)

    # set speed sampled from a Normal distribution
    def init_normal_speed(self):
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
        elif normal:    self.init_normal_speed()
        else:           self.rand_speed()

    # set initial lane and lane position
    def init_place(self, lane, lane_pos):
        lane     = lane     if     lane != -1 else self.rand_lane()
        lane_pos = lane_pos if lane_pos != -1 else self.rand_lane_pos()

        x, y = self.lane_center_to_pixel_pos(lane, lane_pos)

        while (self.is_collision(x, y, self.heading)):
            lane     = self.rand_lane()
            lane_pos = self.rand_lane_pos()
            x, y = self.lane_center_to_pixel_pos(lane, lane_pos)

        self.lane     = lane
        self.lane_pos = lane_pos
    

    def __eq__(self, other):
        return self.id == other.id

    # STRING/PRINTING

    def __str__(self):
        feat = self.get_feature()

        feat_len    = len(feat)
        my_id       = feat[feat_len - 7]
        my_lane     = feat[feat_len - 6]
        my_lane_pos = feat[feat_len - 5]
        my_heading  = feat[feat_len - 4]
        my_speed    = feat[feat_len - 3]
        my_accel    = feat[feat_len - 2]
        my_steering_angle = feat[feat_len - 1]

        res = ("Features of car id = %d: \n " % my_id)
        res += ("Lane: %d. Lane Pos: %d.\n" % (my_lane, my_lane_pos))
        res += ("Heading: %1.1f. Speed: %1.1f. Accel: %1.1f. Steering Angle: %1.1f \n" % \
            (degrees(my_heading),my_speed,my_accel,degrees(my_steering_angle)))

        lane_strs = ["LEFT", "LEFT", "CURR", "CURR", "RIGHT", "RIGHT"]
        dir_strs = ["AHEAD", "BEHIND"]

        for i in range(0, feat_len - 7, 1):
            lane_str = lane_strs[i % 6]
            dir_str = dir_strs[i % 2]

            res += ("%6s and %6s: (id = %3d, steps away = %3d, speed = %2.1f) \n" % \
                (lane_str, dir_str, feat[i][0], feat[i][1], feat[i][2]))

        return res

    def print_feature(self, feat):

        feat_len    = len(feat)
        my_id       = feat[feat_len - 7]
        my_lane     = feat[feat_len - 6]
        my_lane_pos = feat[feat_len - 5]
        my_heading  = feat[feat_len - 4]
        my_speed    = feat[feat_len - 3]
        my_accel    = feat[feat_len - 2]
        my_steering_angle = feat[feat_len - 1]

        print("Features of car id = %d: \n " % my_id)
        print("Lane: %d. Lane Pos: %d." % (my_lane, my_lane_pos))
        print("Heading: %1.1f. Speed: %1.1f. Accel: %1.1f. Steering Angle: %1.1f \n" % \
            (degrees(my_heading),my_speed,my_accel,degrees(my_steering_angle)))


        lane_strs = ["LEFT", "LEFT", "CURR", "CURR", "RIGHT", "RIGHT"]
        dir_strs = ["AHEAD", "BEHIND"]

        for i in range(0, feat_len - 7, 1):
            lane_str = lane_strs[i % 6]
            dir_str = dir_strs[i % 2]

            print("%6s and %6s: (id = %3d, steps away = %3d, speed = %2.1f) \n" % \
                (lane_str, dir_str, feat[i][0], feat[i][1], feat[i][2]))


    # def print_feature(self, feat):

    #     feat_len    = len(feat)
    #     my_id       = feat[feat_len - 4]
    #     my_speed    = feat[feat_len - 3]
    #     my_lane     = feat[feat_len - 2]
    #     my_lane_pos = feat[feat_len - 1]

    #     print("Features of car id = %d: " % my_id)
    #     print("My speed = %1.1f. Lane: %d, Lane Pos: %d" % \
    #         (my_speed, my_lane, my_lane_pos))

    #     lane_strs = ["LEFT", "LEFT", "CURR", "CURR", "RIGHT", "RIGHT"]
    #     dir_strs = ["AHEAD", "BEHIND"]

    #     for i in range(0, feat_len - 4, 1):
    #         lane_str = lane_strs[i % 6]
    #         dir_str = dir_strs[i % 2]

    #         print("%6s and %6s: (id = %3d, steps away = %3d, speed = %2.1f)" % \
    #             (lane_str, dir_str, feat[i][0], feat[i][1], feat[i][2]))


    # GENERAL USEFUL functions
    def convert_y(self, y):
        return self.highway.highway_len - y

    def rand_lane(self): 
        return randint(0, self.highway.num_lanes - 1)
    
    def rand_lane_pos(self): 
        return randint(0, self.highway.highway_len - self.WIDTH - 1)
    
    def rand_speed(self): 
        return randint(self.min_speed, self.max_speed)

    def get_pixel_pos(self):
        return (self.x, self.y)

    def pixel_to_lane_pos(self, x, y):
        lane     = int(x / self.highway.lane_width)
        lane_pos = int(round(self.convert_y(y)))

        return (lane, lane_pos)

    # "IS" FUNCTIONS

    def is_legal_lane(self, lane):
        return in_range(lane, 0, self.highway.num_lanes - 1)

    def is_legal_lane_pos(self, lane_pos):
        return in_range(lane, 0, self.highway.highway_len - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)

    # check if rectangle centered at (new_x, new_y) w/given new_angle
    # has a corner in some other car's rectangle
    # go through car lis in highway (ok for small numbers of cars) 

    def rotate_point(self, orig_pt, center_pt, angle):

        (center_x, old_center_y) = center_pt
        (x, old_y) = orig_pt

        # switch y axis to be increasing from bottom up instead of top-down
        center_y = self.highway.highway_len - old_center_y
        y        = self.highway.highway_len - old_y

        # vector from origin to point
        delta_x, delta_y = (x - center_x, y - center_y)

        # perform rotation (multiply rotation matrix)
        # here angle is complement
        new_delta_x = delta_x * cos(angle) - delta_y * sin(angle)
        new_delta_y = delta_x * sin(angle) + delta_y * cos(angle)

        # translate the point back
        new_x = center_x + new_delta_x
        new_y = center_y + new_delta_y

        # change y coord to be increasing top-down
        new_y = self.highway.highway_len - new_y

        return (new_x, new_y)


    def get_corners(self, x, y, angle):
        top_left  = (x - self.WIDTH/2, y - self.HEIGHT/2)
        top_right = (x + self.WIDTH/2, y - self.HEIGHT/2)

        back_left = (x - self.WIDTH/2, y + self.HEIGHT/2)
        back_right= (x + self.WIDTH/2, y + self.HEIGHT/2)

        new_top_left = self.rotate_point(top_left,  (x, y), angle)
        new_top_right= self.rotate_point(top_right, (x, y), angle)

        new_back_left = self.rotate_point(back_left, (x, y), angle)
        new_back_right= self.rotate_point(back_right,(x, y), angle)

        return (new_top_left, new_top_right, new_back_left, new_back_right)

    def is_collision(self, new_x, new_y, new_heading):
        new_angle = pi/2 - new_heading # angle is angle from y-axis
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            self.get_corners(new_x, new_y, new_angle)

        # see if corners collide with any other car on the road
        for car in self.highway.car_list:
            if car == self:
                continue
            # Rect(left, top, width, height)
            (left, top) = center_to_upper_left(self, car.x, car.y)
            car_rect = pygame.Rect(left, top, self.WIDTH, self.HEIGHT)
            
            collision = car_rect.collidepoint(new_top_left) or \
                        car_rect.collidepoint(new_top_right) or \
                        car_rect.collidepoint(new_back_left) or \
                        car_rect.collidepoint(new_back_right)

            if collision:
                lane, lane_pos = self.pixel_to_lane_pos(new_x, new_y)
                print("car has collision: ", self.id, lane, lane_pos)
                print(car_rect.collidepoint(new_top_left))
                print(car_rect.collidepoint(new_top_right))
                print(car_rect.collidepoint(new_back_left))
                print(car_rect.collidepoint(new_back_right))
                return True
        return False


    def legal_pos(self, new_x, new_y, new_heading):
        new_angle = pi/2 - new_heading # angle is angle from y-axis
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            self.get_corners(new_x, new_y, new_angle)

        # see if corners collide with highway
        
        # Rect(left, top, width, height)
        (left, top) = (0,0)
        highway_rect = pygame.Rect(left,top,self.highway.WIDTH, self.highway.HEIGHT)
        
        within_highway = highway_rect.collidepoint(new_top_left) and \
                    highway_rect.collidepoint(new_top_right) and \
                    highway_rect.collidepoint(new_back_left) and \
                    highway_rect.collidepoint(new_back_right)

        return within_highway
            



    def dist_to_road_boundary(self):
        return in_range(self.x, 0, self.highway.highway_len) and \
            in_range(self.y, 0, self.highway.num_lanes*self.highway.lane_height)

    def dist_to_lane_boundary(self):
        pass
        # front_left  = self.y + self. 
        # front_right =
        # back_left   = 
        # back_right  =  

    # ROTATE CAR IMAGE

    # rotate car image around center
    def rotate(self):
        new_angle = -1 * (90 - degrees(self.heading)) # angle is degrees from y-axis
        # print("new angle", new_angle)
        self.image_car = pygame.transform.rotate(self.straight_image_car,new_angle)
        rect = self.image_car.get_rect()
        rect.center = (self.x, self.y)  

    # edge case, two blinkers
    def toggle_image(self):
        self.file_name = self.original_file_name
        
        if self.right_blinker:
            self.file_name = self.original_file_name + "_right"
        
        if self.left_blinker:
            self.file_name = self.original_file_name + "_left"
        
        if self.right_blinker and self.left_blinker:
            self.file_name = self.original_file_name + "_both"
        
        file = self.file_name + self.file_ext
        self.image_car = pygame.image.load(file).convert_alpha()
        self.straight_image_car = self.image_car
   
    def toggle_blinker(self, blinker):
        if blinker == RIGHT_BLINKER:
            self.right_blinker = not self.right_blinker
        
        if blinker == LEFT_BLINKER:
            self.left_blinker = not self.left_blinker

        self.toggle_image()

    # DRAWING function

    def draw(self, screen):
        (center_x, center_y) = self.get_pixel_pos()
        upper_left_pos = center_to_upper_left(self, center_x, center_y)
        
        screen.blit(self.image_car, upper_left_pos)
        # draw center of car
        # pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), 10, 0)




#  # straight collision
# def is_collision(self, new_lane, new_lane_pos):
#     behind_pos = max(0,new_lane_pos - self.WIDTH)
#     ahead_pos =  min(new_lane_pos + self.WIDTH, self.highway.highway_len-1)

#     my_idx      = self.highway.pos_to_idx(new_lane, new_lane_pos)
#     behind_idx  = self.highway.pos_to_idx(new_lane, behind_pos)
#     ahead_idx   = self.highway.pos_to_idx(new_lane, ahead_pos)

#     no_crash = True
#     curr_idx = behind_idx
    
#     while (no_crash and curr_idx <= ahead_idx):
#         neighbor = self.highway.idx_to_state(curr_idx)
#         no_crash = (neighbor == (-1, -1)) or (neighbor[0] == self.id)
#         curr_idx += 1

#         if not no_crash:
#             print("crash car idx %d" % (curr_idx - 1))

#     if (not no_crash):
#         print ("collision occured, car id %d" % self.id)
#     return (not no_crash)
