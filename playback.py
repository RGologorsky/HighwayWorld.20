# contains Playback functions: storing/writing time series, drawing, and 
# calling the draw function in sync with event queue

import pygame
import pickle
import itertools
import pygame

from datetime import datetime

from math import degrees

from constants import *
from helpers import *

# so that Highway & Cars can be drawn
from highway_mixin import HighwayMixin 
from abstract_car_mixin import AbstractCarMixin

# Drawable objects inherit all the car and highway draw methods
class DrawableCar(AbstractCarMixin):
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

class DrawableHighway(HighwayMixin):

    @staticmethod    
    def get_drawable_car_list(car_list):
        return list(map((lambda x: DrawableCar(x)), car_list))

    def __init__(self, highway_param, highway_car_list):
        for key in highway_param:
            setattr(self, key, highway_param[key])
        self.car_list = self.get_drawable_car_list(highway_car_list)

class Playback(object):

    # writing constants
    pickle_file_start = "recorded_data/data_"

    @classmethod
    def write_recorded_data(cls, highway_data):
        time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        pickle_file = cls.pickle_file_start + time
        with open(pickle_file, "wb") as file:
           pickle.dump(highway_data, file)

    @classmethod
    def get_recorded_data(cls, time):
        pickle_file = cls.pickle_file_start + time
        (highway_param, highway_data) = pickle.load(open(pickle_file, 'rb'))
        return (highway_param, highway_data)


    @classmethod
    def draw_highway_snapshot(cls, screen, highway_param, highway_car_list):
        # consolidate param & car list into highway "object" (attribute access)
        screen.fill(background_color)
        playback_highway = DrawableHighway(highway_param, highway_car_list)
        playback_highway.draw(screen, draw_features = False, is_playback = True)
        pygame.display.flip()
