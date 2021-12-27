from model.util import load_image
import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Floor1(Floor):
    image = load_image('floor_1')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor2(Floor):
    image = load_image('floor_2')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor2.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor3(Floor):
    image = load_image('floor_3')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Floor3.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y