import itertools
from   math import pi
from random import randint

from constants import *
from   helpers import *

from abstract_car_mixin import AbstractCarMixin
from abc import ABCMeta

# kinematic bicycle model, center of gravity at center of car
from dynamics_model import *

from collections import namedtuple

# not efficient 
from copy import deepcopy

class AbstractCar(AbstractCarMixin, object):

    __metaclass__ = ABCMeta

    counter = itertools.count(1)
    
    min_speed = 0
    max_speed = 10
    
    # resets the class counter variable, which is used to assign unique ID's
    def reset_counter():
        AbstractCar.counter = itertools.count(1)

    """ 
    AbstractCar Parameters:

    id is a class-generated identifier used for car object equality testing
    role is used to identify car roles in the scenario (e.g. agent car)
    highway =car's highway object, simulator =car's control interface instance
    heading is measured in radians from the x-axis counter-clockwise
    car image is the car's curren image (changes depending on blinkers)
    straight (unrotated) car image is used to generate rotated car image
    WIDTH, HEIGHT are used to mathematically calculate motion and collision
    lane = current lane, discrete, 0-indexed.
    x = x-coordinate the car's pixel center (float)
    lane pos = current y-position in the lane, growing from bottom to top
    y = y-coordinate corresponding to Pygame, y-axis grows from top to bottom
    right/left blinker = indicator whether the right/left blinker is on
    l_r, l_f = distance to rear/front axle from the center of mass
    
    Car helper functions are located in AbstractCarMixin.
    Derived car classes are in car_class.py
    """

    def __init__(self, highway, simulator=None, lane=-1, lane_pos=-1, speed=-1,role="None"):
        self.id           = next(self.counter)
        self.role         = role

        self.highway      = highway
        self.simulator    = simulator

        self.heading    = pi/2 # 90 degrees from x-axis

        # init car image and straight car image, req: file_name, file_ext init
        self.init_car_images()

        # set width, height
        if not hasattr(self, "WIDTH") or not hasattr(self, "HEIGHT"):
            self.WIDTH, self.HEIGHT = self.straight_image_car.get_rect().size


        # init (x, y, lane, lane_pos) with given inputs or random. 
        self.init_place(lane, lane_pos)
        self.init_pixel_pos()

        # init speed with given speed, random, or normal
        # normal: speed ~ normal disribution w/mean governed by lane
        self.init_speed(speed, normal=True)

        # blinkers
        self.right_blinker = False
        self.left_blinker  = False
 
        # Center of mass = middle.
        self.l_r = self.HEIGHT * 0.50
        self.l_f = self.HEIGHT * 0.50


        # update highway
        self.highway.add_car(self)

    # get the car state, here all non-object car variables.
    # current control inputs (accel, steering angle) are added to car state
    def get_all_car_state(self):
        # dont save objects, save values
        no_keys = ["simulator", "highway", "image_car", "straight_image_car"]
        d = {key:val for key, val in self.__dict__.items() if key not in no_keys}
        d['image_file'] = self.file_name + self.file_ext
        d['u1'] = self.simulator.u1
        d['u2'] = self.simulator.u2

        return d
    
    # given a (perhaps rotated) car, return smallest distance along x or y-axis
    # to the given point.  
    def smallest_dist_to_point(self, pos, y_axis=True):
        (x, y) = pos

        (top_left, top_right, back_left, back_right) = \
            get_corners(self.x, self.y, self.heading, self.WIDTH, self.HEIGHT)

        (x1, y1) = top_left
        (x2, y2) = top_right
        (x3, y3) = back_left
        (x4, y4) = back_right

        if y_axis:
            return min(abs(y - y1), abs(y - y2), abs(y - y3), abs(y - y4))
        if x_axis:
            return min(abs(x - x1), abs(x - x2), abs(x - x3), abs(x - x4))




    # def get_car_state(self):
    #     # in test scenario, just two cars
    #     for car in self.highway.car_list:
    #         car.
    #     # want gap size to ahead, gap size to behind
    #     # and speeds

    #     closest_cars.append(self.id)
    #     closest_cars.append(self.lane)
    #     closest_cars.append(self.lane_pos)
    #     closest_cars.append(self.heading)
    #     closest_cars.append(self.speed)
    #     closest_cars.append(self.simulator.u1)
    #     closest_cars.append(self.simulator.u2)

    #     # u1 = current accel, u2 = current steering angle
    #     d['u1'] = self.simulator.u1
    #     d['u2'] = self.simulator.u2
    #     d['heading'] = self.heading
    #     d['']




    # if necessary, set speed to ahead car speed to maintain distance 
    # set acceleration to 0
    def check_distance(self):
        ahead_pos = self.lane_pos + self.HEIGHT + self.keep_distance
        
        car_in_front = False
        for car in self.highway.car_list:
            if (car.lane == self.lane and \
                in_range(car.lane_pos, self.lane_pos, ahead_pos)):
                car_in_front = True
                self.speed = min(self.speed, car.speed) 
                self.simulator.u1 = 0 # set acceleration

        # if no car in front, maintain preferred speed
        if not car_in_front:
            self.speed = self.preferred_speed

            
    def move(self, allow_collision = False, check_distance = False, \
                check_legal_pos = False):

        (new_x, new_y, new_speed, new_heading) = \
            next_step(self.x, self.y, self.speed, self.heading, \
                self.simulator.u1, self.simulator.u2, self.l_r, self.l_f)

        new_lane, new_lane_pos = self.pixel_to_lane_pos(new_x, new_y)


        is_collision = self.is_collision(new_x, new_y, new_heading)


        if allow_collision or not is_collision:
            self.heading = new_heading

            if self.is_legal_speed(new_speed):
                self.speed = new_speed

            if check_distance:
                self.check_distance()


            
            # CHECK IF LEGAL LANE, POSIION (if needed)
            is_legal_pos = self.is_legal_pos(new_x, new_y, new_heading)

            if not check_legal_pos or is_legal_pos:
                    self.x, self.y           = new_x, new_y
                    self.lane, self.lane_pos = new_lane, new_lane_pos
            self.rotate()
                
        return is_collision
        

    # feature = list (id, #steps away, speed) for cars ahead/behind and 
    # left, current, right lanes. At end, agent's id, speed, lane, & lane pos.
    # u1 = acceleration, u2 = steering angle (radians)
    def get_feature(self):
        closest_cars = self.highway.get_closest_cars(self.lane, self.lane_pos)
        closest_cars.append(self.id)
        closest_cars.append(self.lane)
        closest_cars.append(self.lane_pos)
        closest_cars.append(self.heading)
        closest_cars.append(self.speed)
        closest_cars.append(self.simulator.u1)
        closest_cars.append(self.simulator.u2)
        # closest_cars.append(self.is_within_lane())
        # print("within lane? id = %d. Within lane = %r" % (self.id, self.is_within_lane()))
        return closest_cars


    def set_car_back(self, amt_back):        
        new_y = self.y + amt_back
        new_lane, new_lane_pos = self.pixel_to_lane_pos(self.x, new_y)

        # cars can disappear behind start of highway (lane_pos < 0)

        self.y        = new_y
        self.lane_pos = new_lane_pos

    def set_all_cars_back(self, amt_back):   
        self.highway.down_speed = amt_back 
        self.highway.set_all_back(amt_back)



    # Keyboard input or regulated speed change to car in front
    def change_lane(self, dir):
        new_lane = self.lane + dir
        
        if self.is_legal_lane(new_lane):

            self.lane = new_lane
            self.x    += dir * self.highway.lane_width
        
    def change_speed(self, speed_change):
        new_speed = self.speed + speed_change
        
        if self.is_legal_speed(new_speed): 
            self.speed = new_speed

    def get_simulate_step_param(self):
        return (self.x, self.y, self.speed, \
                self.heading, self.simulator.u1, self.simulator.u2, \
                self.l_r, self.l_f, self.WIDTH, self.HEIGHT)

    @classmethod    
    def simulate_step(cls, simulate_step_param):
        x, y, v, psi, u1, u2, l_r, l_f, width, height = simulate_step_param
        
        new_x, new_y, new_v, new_psi = \
            next_step(x, y, v, psi, u1, u2, l_r, l_f)


        new_simulate_step_param = (new_x, new_y, new_v, new_psi, \
            u1, u2, l_r, l_f, width, height)

        return new_simulate_step_param
