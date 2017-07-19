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

# game events helpers
def is_quit(event):
    return (event.type == pygame.QUIT) or \
        ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE))

def is_restart(event, PAUSE):
    return event.type == pygame.JOYBUTTONDOWN and event.button == R

def is_pause_pressed(event):
    return ((event.type == pygame.KEYDOWN and event.key == pygame.K_p) or \
        event.type == pygame.JOYBUTTONDOWN and event.button == P)

def is_blinker(event):
    return event.type == pygame.JOYBUTTONDOWN and \
        (event.button == LEFT_BLINKER or event.button == RIGHT_BLINKER)
