import sys
import pygame
from model.util import load_image

WIDTH = 800
HEIGHT = 600
FPS = 50


class Button(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("600x600_button_1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 0
        self.image2 = load_image("600x600_button_2.png")

    def change_sprite(self):
        self.image = self.image2


def terminate():
    pygame.quit()
    sys.exit()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def start_screen(screen, clock):
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))

    screen.blit(fon, (0, 0))
    sg = pygame.sprite.Group()
    button = Button(sg)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button.change_sprite()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    return  # начинаем игру
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        sg.draw(screen)
        sg.update()
        pygame.display.flip()
        clock.tick(FPS)
