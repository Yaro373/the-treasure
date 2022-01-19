import pygame
from model.util import load_image, terminate

WIDTH = 800
HEIGHT = 600
FPS = 50


def lose_screen():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('you_lose.png'), (WIDTH, HEIGHT))

    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)
