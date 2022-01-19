import model.data_saver
import pygame
import sys
import os


def load_image(name):
    fullname = os.path.join('resources', 'sprites', name)
    image = pygame.image.load(fullname)
    return image


def seconds_to_milliseconds(seconds):
    return seconds * 1000


def terminate():
    model.data_saver.DataSaver.save()
    pygame.quit()
    sys.exit()
