import pygame
import sys
import main
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', 'sprites', name)
    image = pygame.image.load(fullname)
    return image