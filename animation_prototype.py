import os
import sys

import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('resources\\sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, surface):
        super().__init__(surface)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def set_cords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_sheet_id(self):
        return self.cur_frame

    def get_sheet_count(self):
        return len(self.frames)


class MainCharacter:
    def __init__(self, x, y):
        self.body_cords = [-0.5, 1, 1, 3, 1, -1, 0, 2, 3, 3]
        # где должно находиться тело на каждый шаг анимации
        self.x = x
        self.y = y
        self.character_group = pygame.sprite.Group()
        self.legs = AnimatedSprite(load_image("128_128_legs_animation.png"), 10, 1, 128, 128,
                                   self.character_group)
        self.body = AnimatedSprite(load_image("128_128_attack_animation.png"), 8, 1, 128, 128,
                                   self.character_group)
        self.move(self.x, self.y)
        self.update()

    def move(self, x, y):
        self.x = x
        self.y = y
        self.legs.rect.x = self.x
        self.legs.rect.y = self.y
        self.body.rect.x = self.x
        self.body.rect.y = self.y - self.body_cords[self.legs.cur_frame]

    def draw(self, surface):
        self.character_group.draw(surface)

    def update(self):
        # сдесь регулируется анимация персонажа
        print(self.legs.cur_frame)
        y = self.y - self.body_cords[self.legs.cur_frame]

        self.body.rect.y = y
        self.character_group.update()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    loop = True
    clock = pygame.time.Clock()
    character = MainCharacter(0, 0)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        screen.fill((0, 0, 0))
        character.draw(screen)
        character.update()
        character.move(character.x + 1, character.y + 1)
        # ...
        clock.tick(10)
        pygame.display.flip()
    pygame.quit()
