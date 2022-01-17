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
        self.prev_sheet = 0
        # возможно это кастыль, но пихаем каждый анимирорванныфй спрайт в свою группу,
        # чтобы контролировать их отрисовку по отдельности
        self.legs_group = pygame.sprite.Group()
        self.sword_attack_group = pygame.sprite.Group()
        self.sword_run_group = pygame.sprite.Group()
        self.bow_group = pygame.sprite.Group()
        self.lamp_group = pygame.sprite.Group()
        self.nothing_group = pygame.sprite.Group()
        self.legs = AnimatedSprite(load_image("128_128_legs_animation.png"), 10, 1, 128, 128,
                                   self.legs_group)
        self.body_sword_attack = AnimatedSprite(load_image("128_128_attack_animation.png"), 8, 1, 128, 128,
                                   self.sword_attack_group)
        self.body = AnimatedSprite(load_image("128_128_body_animation.png"), 10, 1, 128, 128,
                                   self.nothing_group)
        self.body_sword_run = AnimatedSprite(load_image("128_128_sword_run_animation.png"), 5, 1, 128, 128,
                                   self.sword_run_group)
        self.body_lamp_run = AnimatedSprite(load_image("128_128_oil_lamp_body_animation.png"), 5, 1, 128, 128,
                                   self.lamp_group)
        self.mode = 0 # 0 - nothing, 1 - sword, 2 - sword_run, 3 - lamp, 4 - bow run, 5 - bow shoot
        self.move(self.x, self.y)
        self.update()

    def move(self, x, y):
        self.x = x
        self.y = y
        self.legs.rect.x = self.x
        self.legs.rect.y = self.y
        self.body.rect.x = self.x
        self.body.rect.y = self.y - self.body_cords[self.legs.cur_frame]

    def attack(self):
        self.mode = 1
        self.update()
        # todo сделать так, чтобы персонаж атаковал 1 раз,
        # todo а затем возвращался в предыдущее состояние

    def set_mode(self, mode):
        self.mode = mode
        self.update()

    def draw(self, surface):
        self.legs_group.draw(surface)
        if self.mode == 0:
            self.nothing_group.draw(surface)
        if self.mode == 1:
            self.sword_attack_group.draw(surface)
        if self.mode == 2:
            self.sword_run_group.draw(surface)
        if self.mode == 3:
            self.lamp_group.draw(surface)

    def update(self):
        cur_sprite = None
        self.legs.update()  # обновляем ноги
        if self.mode == 0:
            cur_sprite = self.body
            cur_sprite.cur_frame = self.legs.cur_frame
        elif self.mode == 1:
            cur_sprite = self.body_sword_attack
        elif self.mode == 2:
            cur_sprite = self.body_sword_run
            cur_sprite.cur_frame = self.legs.cur_frame % 5
        elif self.mode == 3:
            cur_sprite = self.body_lamp_run
            cur_sprite.cur_frame = self.legs.cur_frame % 5
        # сдесь регулируется анимация персонажа
        y = self.y - self.body_cords[self.legs.cur_frame]
        x = self.x

        cur_sprite.rect.y = y
        cur_sprite.rect.x = x
        self.legs.update()
        cur_sprite.update()


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    character.set_mode(0)
                if event.key == pygame.K_2:
                    character.set_mode(1)
                if event.key == pygame.K_3:
                    character.set_mode(2)
                if event.key == pygame.K_4:
                    character.set_mode(3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    character.attack()

        screen.fill((0, 0, 0))
        character.draw(screen)
        character.update()
        character.move(character.x + 1, character.y + 1)
        # ...
        clock.tick(10)
        pygame.display.flip()
    pygame.quit()
