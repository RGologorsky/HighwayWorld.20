# Abstract Car Mixin
# general useful functions, constants
import pygame
from constants import *
from random import randint

class AbstractCarMixin(object):
    
    """ Car image size width = 228, height = 128 """
    # WIDTH = 104 #228
    # HEIGHT = 48 #128

    WIDTH = 48 #228
    HEIGHT = 104 #128

    data = "rotated_data"

    def __eq__(self, other):
        return self.id == other.id

    # STRING/PRINTING

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


    # GENERAL USEFUL functions

    def center_to_upper_left(x, y):
        return (x - AbstractCarMixin.WIDTH/2, \
                y - AbstractCarMixin.HEIGHT/2)

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
        lane_pos = int(round(self.highway.highway_len - y))

        return (lane, lane_pos)

    # "IS" FUNCTIONS

    def is_legal_lane(self, lane):
        return in_range(lane, 0, self.highway.num_lanes - 1)

    def is_legal_speed(self, new_speed):
        return in_range(new_speed, self.min_speed, self.max_speed)


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
        self.image_car = pygame.transform.rotate(self.original_image, -1 * self.angle)
        rect = self.image_car.get_rect()
        rect.center = (self.x, self.y)  

    # DRAWING function

    def draw(self, screen):
        (center_x, center_y) = self.get_pixel_pos()
        upper_left_pos = AbstractCarMixin.center_to_upper_left(center_x, center_y)
        
        screen.blit(self.image_car, upper_left_pos)
        # draw center of car
        pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), 10, 0)
