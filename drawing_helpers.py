import pygame
from constants import *

default_font = pygame.font.SysFont('Arial', 15)
default_font.set_bold(True)
def render_multi_line(screen, text, x, y, font=default_font, text_color=BLACK):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        text_height = font.size(lines[0])[1] 
        screen.blit(font.render(l, 0, text_color), (x, y + text_height*i))
