from model.util import load_image
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Wall1(Wall):
    image = load_image('wall_1')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall2(Wall):
    image = load_image('wall_2')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall3(Wall):
    image = load_image('wall_3')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y