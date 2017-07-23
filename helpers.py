""" Define what engine need """
import pygame
from constants import *
from math import pi, cos, sin, radians

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


# geometry
def rotate_point(orig_pt, center_pt, angle):

    (center_x, center_y) = center_pt
    (x, y) = orig_pt

    # switch y axis to be increasing from bottom up instead of top-down
    # center_y = self.highway.highway_len - old_center_y
    # y        = self.highway.highway_len - old_y

    # vector from origin to point
    # y is switched because of opposite orientation
    delta_x, delta_y = (x - center_x, -(y - center_y))

    # perform rotation (multiply rotation matrix)
    # here angle is complement
    new_delta_x = delta_x * cos(angle) - delta_y * sin(angle)
    new_delta_y = delta_x * sin(angle) + delta_y * cos(angle)

    # translate the point back
    new_x = center_x + new_delta_x
    new_y = center_y - new_delta_y # diff y orientation

    # change y coord to be increasing top-down
    # new_y = self.highway.highway_len - new_y

    return (new_x, new_y)

# gets coreners of rectangle    
def get_corners(x, y, heading, WIDTH, HEIGHT):
        angle = heading - pi/2

        top_left  = (x - WIDTH/2, y - HEIGHT/2)
        top_right = (x + WIDTH/2, y - HEIGHT/2)

        back_left = (x - WIDTH/2, y + HEIGHT/2)
        back_right= (x + WIDTH/2, y + HEIGHT/2)

        new_top_left = rotate_point(top_left,  (x, y), angle)
        new_top_right= rotate_point(top_right, (x, y), angle)

        new_back_left = rotate_point(back_left, (x, y), angle)
        new_back_right= rotate_point(back_right,(x, y), angle)

        return (new_top_left, new_top_right, new_back_left, new_back_right)

def get_car_rect_corners(x, y, heading, WIDTH, HEIGHT):
    A, B, D, C = get_corners(x, y, heading, WIDTH, HEIGHT)
    return A, B, C, D

def vector(ptA, ptB):
    (a, b) = ptA
    (c, d) = ptB

    return (c - a, d - b)

def dot(ptA, ptB):
    (x1, y1) = ptA
    (x2, y2) = ptB

    return x1 * x2 + y1 * y2

# collide point based on
# https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
def collidepoint(rectangle, M):
    A, B, C, D = rectangle

    AB = vector(A, B)
    BC = vector(B, C)

    AM = vector(A, M)
    BM = vector(B, M)

    return (in_range(dot(AB,AM), 0, dot(AB,AB)) and \
            (in_range(dot(BC,BM), 0, dot(BC,BC))))

def is_rect_collision(rect1, rect2):
        A, B, C, D = rect1
        return collidepoint(rect2, A) or \
               collidepoint(rect2, B) or \
               collidepoint(rect2, C) or \
               collidepoint(rect2, D)

# positions is a list of projected (x, y, heading) for every car
def is_crash(positions):
    l = len(positions)
    for i in range(l):
        pos_car_i = positions[i]
        x, y, v, psi, u1, u2, l_r, l_f, width, height = pos_car_i
        rect_i = get_car_rect_corners(x, y, psi, width, height)

        for j in range(i + 1, l):
            
            pos_car_j = positions[j]
            x, y, v, psi, u1, u2, l_r, l_f, width, height = pos_car_j
            rect_j = get_car_rect_corners(x, y, psi, width, height)

            is_collision = is_rect_collision(rect_i, rect_j)

            if is_collision:
                return True
    return False
