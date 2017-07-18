import pygame
from helpers import *
from abstract_car_mixin import AbstractCarMixin

# pygame.sprite.Sprite
class Tree(object):
    image_file = "rotated_data" + "/small_tree_transparent.png"
    WIDTH = 75
    HEIGHT = 118

    def __init__(self, highway_param):
        self.image = pygame.image.load(Tree.image_file).convert_alpha()

        num_lanes, self.highway_len, lane_width = highway_param
        
        self.x = num_lanes * lane_width + Tree.WIDTH/2
        self.y = 0 

    def draw(self, screen):
        (center_x, center_y) = self.x, self.y
        upper_left_pos = center_to_upper_left(self, center_x, center_y)
        screen.blit(self.image, upper_left_pos)

    def set_back(self, amt_back):
        self.y = self.y + amt_back

        if self.y >= self.highway_len:
            self.y = 0

    def get_state(self):
        return (self.x, self.y)
