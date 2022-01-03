import random

from model.util import load_image
from parameters import CELL_SIZE
import view.level
import pygame


class BaseObjectSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dung_x = self.rect.x // CELL_SIZE
        self.dung_y = self.rect.y // CELL_SIZE


class Wall1(BaseObjectSprite):
    image = load_image('64x64_wall_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall1.image, x, y, *group)


class Wall2(BaseObjectSprite):
    image = load_image('64x64_wall_2.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall2.image, x, y, *group)


class Wall3(BaseObjectSprite):
    image = load_image('64x64_wall_3.png')

    def __init__(self, x, y, *group):
        super().__init__(Wall3.image, x, y, *group)


class UnbreakableWall(BaseObjectSprite):
    image = load_image("64x64_wall_3.png")  # todo поменять спрайт

    def __init__(self, x, y, *group):
        super().__init__(Wall3.image, x, y, *group)


class Floor1(BaseObjectSprite):
    image = load_image('64x64_floor_1.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor1.image, x, y, *group)


class Floor2(BaseObjectSprite):
    image = load_image('64x64_floor_2.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor2.image, x, y, *group)


class Floor3(BaseObjectSprite):
    image = load_image('64x64_floor_3.png')

    def __init__(self, x, y, *group):
        super().__init__(Floor3.image, x, y, *group)


class Chest(BaseObjectSprite):
    closed_chest_image = load_image('64x64_chest.png')
    opened_chest_image = load_image('64x64_opened_chest.png')

    def __init__(self, x, y, *group):
        super().__init__(Chest.closed_chest_image, x, y, *group)

    def update(self, event):
        level = view.level.LevelManager.get_current_level()
        if event is not None:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                if (self.dung_x, self.dung_y) == level.character.get_dung_coords() or \
                        (self.dung_x, self.dung_y) == level.character.get_d_dung_coords():
                    self.open_chest()

    def open_chest(self):
        self.image = Chest.opened_chest_image

    def close_chest(self):
        self.image = Chest.closed_chest_image


# TODO
# Ловушка
class Trap(BaseObjectSprite):
    closed_chest_image = None

    def __init__(self, x, y, *group):
        super().__init__(Chest.opened_chest_image, x, y, *group)
