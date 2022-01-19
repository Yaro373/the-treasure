import sys
import pygame
from model.util import load_image
import random

WIDTH = 800
HEIGHT = 600
FPS = 50


class WinChest(pygame.sprite.Sprite):

    def __init__(self, group, width, height):
        self.image = load_image("200x200_win_chest_closed.png")
        self.image_opened = load_image("200x200_win_chest_opened.png")
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.opened = False

    def open(self):
        self.opened = True
        self.image = self.image_opened

class RandomWinItem(pygame.sprite.Sprite):

    def __init__(self, group, width, height):
        self.image = random.choice((load_image("400x400_prize_1.png"),
                                    load_image("400x400_prize_4.png"),
                                    load_image("400x400_prize_5.png"),
                                    load_image("400x400_prize_6.png"),
                                    load_image("400x400_prize_7.png"),
                                    load_image("400x400_prize_8.png"),
                                    load_image("400x400_prize_9.png"),
                                    ))
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.opened = False
        self.rect.x = width
        self.rect.y = height



def terminate():
    pygame.quit()
    sys.exit()


# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()


def win_screen(screen, clock):
    fon = pygame.transform.scale(load_image('you_win.png'), (WIDTH, HEIGHT))
    fon_2 = pygame.transform.scale(load_image('you_win_ogo.png'), (WIDTH, HEIGHT))

    screen.blit(fon, (0, 0))
    sg = pygame.sprite.Group()
    chest = WinChest(sg, 550, 330)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not chest.opened:
                    chest.open()
                    RandomWinItem(sg, 0, 100)

        screen.fill((0, 0, 0))
        if chest.opened:
            screen.blit(fon_2, (0, 0))
        else:
            screen.blit(fon, (0, 0))
        sg.draw(screen)
        sg.update()
        pygame.display.flip()
        clock.tick(FPS)


# win_screen(screen, clock)
