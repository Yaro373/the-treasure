import sys
import pygame
from model.util import load_image
import random

WIDTH = 800
HEIGHT = 600
FPS = 50

def terminate():
    pygame.quit()
    sys.exit()


# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()


def win_screen(screen, clock):
    fon = pygame.transform.scale(load_image('you_lose.png'), (WIDTH, HEIGHT))

    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)


# win_screen(screen, clock)
