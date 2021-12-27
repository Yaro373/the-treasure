from game.model.util import load_image
import pygame


class Floor1(pygame.sprite.Sprite):
    image = load_image('64x64_floor_1.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor2(pygame.sprite.Sprite):
    image = load_image('floor_2.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor2.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor3(pygame.sprite.Sprite):
    image = load_image('floor_3.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor3.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y