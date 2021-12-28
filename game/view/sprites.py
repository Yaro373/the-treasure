from game.model.util import load_image
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall1(Wall):
    image = load_image('64x64_wall_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall1.image, x, y, *group)


class Wall2(Wall):
    image = load_image('64x64_wall_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall2.image, x, y, *group)


class Wall3(Wall):
    image = load_image('64x64_wall_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall3.image, x, y, *group)


class Floor1(Floor):
    image = load_image('64x64_floor_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor1.image, x, y, *group)


class Floor2(Floor):
    image = load_image('64x64_floor_2.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor2.image, x, y*group)


class Floor3(Floor):
    image = load_image('64x64_floor_3.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor3.image, x, y, *group)