""" Define what engine need """
import pygame
from constants import *

# useful functions

def redraw_all(screen, draw_list):
    screen.fill(GREEN)
    for obj in draw_list:
        obj.draw(screen)
    pygame.display.flip()


def render_multi_line(screen, text, x, y, text_color=BLACK):
    font = pygame.font.SysFont('Arial', 15)
    lines = text.splitlines()
    for i, l in enumerate(lines):
        text_height = font.size(lines[0])[1] 
        screen.blit(font.render(l, 0, text_color), (x, y + text_height*i))


def in_range(x, a, b):
    return a <= x and x <= b

def center_to_upper_left(self, x, y):
    return (x - self.WIDTH/2, y - self.HEIGHT/2)
