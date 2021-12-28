from game.model.util import load_image
import pygame


class BaseItemSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
