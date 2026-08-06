import pygame
from os.path import join

pygame.init()
screen = pygame.display.set_mode((1280, 720))
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
pygame.display.set_caption("Space Shooter")