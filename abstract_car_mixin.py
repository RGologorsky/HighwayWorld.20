# Abstract Car Mixin
# general useful functions, constants

import pygame
import numpy as np
from random import randint
from math import pi, radians, degrees, cos, sin
from constants import *
from helpers import *


class AbstractCarMixin(object):
    
    WIDTH = 44 #228
    HEIGHT = 100 #128

    data = "images"

    # init functions
    def lane_to_x_boundary(self, lane, left = True):
        if left:
            return self.highway.lane_width * lane
        # if right
        return self.highway.lane_width * (lane + 1)


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

        if   self.lane == 0:                          mu = 8
        elif self.lane == self.highway.num_lanes - 1: mu = 6
        else:                                         mu = 5

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


    # GENERAL USEFUL functions

    # converts y from pygame coordinate (y increasing from top-down) to
    # conventional y axis (y increasing from bottom-up)
    def convert_y(self, y):
        return self.highway.highway_len - y

    # returns a random lane from the available highway lanes
    def rand_lane(self): 
        return randint(0, self.highway.num_lanes - 1)
    
    # returns a random lane position from the possible lane positions
    def rand_lane_pos(self): 
        return randint(0, self.highway.highway_len - self.WIDTH - 1)
    
    # returns a random speed between the min and max speed (inclusive)
    def rand_speed(self): 
        return randint(self.min_speed, self.max_speed)

    # returns the car's position (x, y) in terms of pixel position
    def get_pixel_pos(self):
        return (self.x, self.y)

    # converts the pixel (x, y) position to a (lane number, lane position)
    def pixel_to_lane_pos(self, x, y):
        lane     = int(x / self.highway.lane_width)
        lane_pos = int(round(self.convert_y(y)))

        return (lane, lane_pos)

    # "IS" FUNCTIONS

    # returns whether the given lane is a legal lane
    def is_legal_lane(self, lane):
        return in_range(lane, 0, self.highway.num_lanes - 1)

     # returns whether the given lane position is a legal lane position
    def is_legal_lane_pos(self, lane_pos):
        return in_range(lane, 0, self.highway.highway_len - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)


    def is_collision(self, new_x, new_y, new_heading):
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            get_corners(new_x, new_y, new_heading, self.WIDTH, self.HEIGHT)

        # see if corners collide with any other car on the road
        for car in self.highway.car_list:
            if car == self:
                continue
            
            car_rect = get_car_rect_corners(car.x, car.y, car.heading, \
                                            car.WIDTH, car.HEIGHT)

            collision = collidepoint(car_rect, new_top_left) or \
                        collidepoint(car_rect, new_top_right) or \
                        collidepoint(car_rect, new_back_left) or \
                        collidepoint(car_rect, new_back_right)

            # (left, top) = center_to_upper_left(self, car.x, car.y)
            # car_rect = pygame.Rect(left, top, self.WIDTH, self.HEIGHT)
            
            # collision = car_rect.collidepoint(new_top_left) or \
            #             car_rect.collidepoint(new_top_right) or \
            #             car_rect.collidepoint(new_back_left) or \
            #             car_rect.collidepoint(new_back_right)

            if collision:
                lane, lane_pos = self.pixel_to_lane_pos(new_x, new_y)
                print("car has collision: ", self.id, lane, lane_pos)
                # print(car_rect.collidepoint(new_top_left))
                # print(car_rect.collidepoint(new_top_right))
                # print(car_rect.collidepoint(new_back_left))
                # print(car_rect.collidepoint(new_back_right))
                return True
        return False


    def is_legal_pos(self, new_x, new_y, new_heading):
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            get_corners(new_x, new_y, new_heading, self.WIDTH, self.HEIGHT)

        # see if corners collide with highway
        
        # Rect(left, top, width, height)
        (left, top) = (0,0)
        highway_rect = pygame.Rect(left,top,self.highway.WIDTH, self.highway.HEIGHT)
        
        within_highway = highway_rect.collidepoint(new_top_left) and \
                    highway_rect.collidepoint(new_top_right) and \
                    highway_rect.collidepoint(new_back_left) and \
                    highway_rect.collidepoint(new_back_right)

        # if not within_highway:
        #     new_x, new_y = new_back_left
        #     lane, lane_pos = self.pixel_to_lane_pos(new_x, new_y)
        #     # print("lane %d, lane pos %d" % (lane, lane_pos))
        #     # print("not within highway: ", self.id)
        #     print(highway_rect.collidepoint(new_top_left))
        #     print(highway_rect.collidepoint(new_top_right))
        #     print(highway_rect.collidepoint(new_back_left))
        #     print(highway_rect.collidepoint(new_back_right))
        return within_highway
            

    def is_point_in_lane(self, pt, lane):
        (x, y) = pt
        pt_lane, pt_lane_pos = self.pixel_to_lane_pos(x, y)
        return (pt_lane == lane) 

    def is_within_lane(self):
        (top_left, top_right, back_left, back_right) = \
            self.get_corners(self.x, self.y, self.heading)

        return (self.is_point_in_lane(top_left, self.lane) and \
                self.is_point_in_lane(top_right, self.lane) and \
                self.is_point_in_lane(back_left, self.lane) and \
                self.is_point_in_lane(back_right, self.lane))

    # left = boolean, left or right lane boundary
    def dist_to_lane_boundary(self, lane, left):

        x_boundary = self.lane_to_x_boundary(lane, left)

        (top_left, top_right, back_left, back_right) = \
            get_corners(self.x, self.y, self.heading, self.WIDTH, self.HEIGHT)

        (x1, y1) = top_left
        (x2, y2) = top_right
        (x3, y3) = back_left
        (x4, y4) = back_right

        if left:
            return (min(x1, x2, x3, x4) - x_boundary)

        # if right
        return (x_boundary - max(x1, x2, x3, x4))


    # left is a boolean, left or right road boundary
    def dist_to_road_boundary(self, left):
        if left:
            return self.dist_to_lane_boundary(self, 0, left)
        # if right
        return self.dist_to_lane_boundary(self, self.highway.num_lanes - 1, left)


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
        self.straight_image_car = pygame.image.load(file).convert_alpha()
        self.image_car = self.straight_image_car
        self.rotate()
   
    def toggle_blinker(self, blinker):
        if blinker == RIGHT_BLINKER:
            self.right_blinker = not self.right_blinker
        
        if blinker == LEFT_BLINKER:
            self.left_blinker = not self.left_blinker

        self.toggle_image()

    # DRAWING function

    def int_coord(self, coord):
        x, y = coord
        return (int(x), int(y))

    def draw(self, screen):
        (center_x, center_y) = self.get_pixel_pos()

        image_rect = self.image_car.get_rect()
        image_rect.centerx = center_x
        image_rect.centery = center_y

        screen.blit(self.image_car, image_rect)        
        
        # draw center of car
        pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), 5, 0)

        # draw corners of car
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            get_corners(self.x, self.y, self.heading, self.WIDTH, self.HEIGHT)

        pygame.draw.circle(screen, BLACK, self.int_coord(new_top_left), 5, 0)
        pygame.draw.circle(screen, BLACK, self.int_coord(new_top_right), 5, 0)
        pygame.draw.circle(screen, BLACK, self.int_coord(new_back_left), 5, 0)
        pygame.draw.circle(screen, BLACK, self.int_coord(new_back_right), 5, 0)
