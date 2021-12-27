from game.model.util import load_image
import pygame


class Wall1(pygame.sprite.Sprite):
    image = load_image('64x64_wall_1.png')

    def __init__(self, x, y, *group):
        print(group)
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall2(pygame.sprite.Sprite):
    image = load_image('wall_2.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall3(pygame.sprite.Sprite):
    image = load_image('wall_3.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Wall1.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y