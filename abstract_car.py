import itertools
from   math import pi
from random import randint

from constants import *
from   helpers import *

from abstract_car_mixin import AbstractCarMixin
from abc import ABCMeta

# kinematic bicycle model, center of gravity at center of car
from dynamics_model import *

class AbstractCar(AbstractCarMixin, object):

    __metaclass__ = ABCMeta

    counter = itertools.count(1)
    
    min_speed = 0.1
    max_speed = 20
    
    # init functions
    def reset_counter():
        AbstractCar.counter = itertools.count(1)

   
    def __init__(self, highway, simulator=None, lane=-1, lane_pos=-1, speed=-1):
        self.id           = next(self.counter)
        
        self.highway      = highway
        self.simulator    = simulator

        self.heading    = pi/2 # 90 degrees from x-axis

        # init (x, y, lane, lane_pos) with given inputs or random. 
        self.init_place(lane, lane_pos)
        self.init_pixel_pos()

        # init speed with given speed, random, or normal
        # normal: speed ~ normal disribution w/mean governed by lane
        self.init_speed(speed, normal=True)

        # Center of mass = middle.
        self.l_r = self.HEIGHT/2.0
        self.l_f = self.HEIGHT/2.0

        # blinkers
        self.right_blinker = False
        self.left_blinker  = False

        # file images
        file = self.file_name + self.file_ext
        self.image_car = pygame.image.load(file).convert_alpha()
        self.straight_image_car = self.image_car

        # update highway
        self.highway.add_car(self)


    def move(self, allow_collision = False):

        # convert y to increasing bottom-up
        # print("heading", self.heading)
        # print("heading (deg)", degrees(self.heading))
        y = self.convert_y(self.y)

        (new_x, new_y, new_speed, new_heading) = \
            next_step(self.x, y, self.speed, self.heading, \
                self.simulator.u1, self.simulator.u2, self.l_r, self.l_f)

        # convert y back
        new_y = self.convert_y(new_y)

        new_lane, new_lane_pos = self.pixel_to_lane_pos(new_x, new_y)

      

        is_collision = self.is_collision(new_x, new_y, new_heading)


        if allow_collision or not is_collision:
            self.speed               = new_speed
            
             # CHECK IF LEGAL SPEED, LANE, POSIION            
            if self.legal_pos(new_x, new_y, new_heading):
                self.x, self.y           = new_x, new_y
                self.lane, self.lane_pos = new_lane, new_lane_pos
                self.heading             = new_heading
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
        return closest_cars


    def set_car_back(self, amt_back):        
        new_y = self.y + amt_back
        new_lane, new_lane_pos = self.pixel_to_lane_pos(self.x, new_y)

        # cars can disappear behind start of highway (lane_pos < 0)

        self.y        = new_y
        self.lane_pos = new_lane_pos

    def set_all_cars_back(self):
        amt_back = self.speed
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



