from model.util import load_image
import pygame


class BaseItemSprite(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()


class Tea(BaseItemSprite):
    image = load_image('32x32_tea.png')

    def __init__(self, num, *group):
        super().__init__(Tea.image, *group)
        self.num = num

    def set_num(self, num):
        self.num = num

    def get_num(self):
        return self.num