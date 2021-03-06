import os
import sys
import pygame
import random
import view.level
import view.util_sprites
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


class Arrow(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, *group):
        super().__init__(*group)
        self.direction = direction
        self.speed = 5
        self.level = view.level.LevelManager.get_current_level()

        self.group = pygame.sprite.Group()
        self.image = load_image('arrow1.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        if self.direction in (2, 4):
            self.rect.y += random.randint(-4, 4)
        elif self.direction in (1, 3):
            self.rect.x += random.randint(-4, 4)

    def update(self):
        if self.direction == 1:
            self.rect.y -= self.speed
        elif self.direction == 2:
            self.rect.x += self.speed
        elif self.direction == 3:
            self.rect.y += self.speed
        elif self.direction == 4:
            self.rect.x -= self.speed


class AnimatedGhostBall(pygame.sprite.Sprite):
    frame1 = load_image('32x32_ghostball_frame1.png')
    frame2 = load_image('32x32_ghostball_frame2.png')
    frame3 = load_image('32x32_ghostball_frame3.png')
    frame4 = load_image('32x32_ghostball_frame4.png')
    frames = [frame1, frame2, frame3, frame4]

    def __init__(self, x, y, surface):
        super().__init__(surface)
        self.frames = AnimatedGhostBall.frames
        self.surface = surface
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, surface):
        super().__init__(surface[0])
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

        self.x = x
        self.y = y
        self.prev_sheet = 0

        self.legs_group = pygame.sprite.Group()
        self.sword_attack_group = pygame.sprite.Group()
        self.sword_run_group = pygame.sprite.Group()
        self.bow_group = pygame.sprite.Group()
        self.shoot_group = pygame.sprite.Group()
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
        self.body_shoot = AnimatedSprite(load_image("128_128_shoot_animation.png"), 10, 1, 128, 128,
                                   self.shoot_group)
        self.body_bow_run = AnimatedSprite(load_image("128_128_bow_run_animation.png"), 5, 1, 128, 128,
                                   self.bow_group)
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

        self.body_shoot.rect.x = self.x
        self.body_shoot.rect.y = self.y - self.body_cords[self.legs.cur_frame]

        self.body_bow_run.rect.x = self.x
        self.body_bow_run.rect.y = self.y - self.body_cords[self.legs.cur_frame]

        self.body_lamp_run.rect.x = self.x
        self.body_lamp_run.rect.y = self.y - self.body_cords[self.legs.cur_frame]

        self.body_sword_run.rect.x = self.x
        self.body_sword_run.rect.y = self.y - self.body_cords[self.legs.cur_frame]

        self.body_sword_attack.rect.x = self.x
        self.body_sword_attack.rect.y = self.y - self.body_cords[self.legs.cur_frame]


    def attack(self):
        if self.mode == 2:
            self.mode = 1
            self.body_sword_attack.cur_frame = 0
            self.prev_sheet = 0
            self.update()
        if self.mode == 4:
            self.mode = 5
            self.body_sword_attack.cur_frame = 0
            self.prev_sheet = 0
            self.update()

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
        if self.mode == 4:
            self.bow_group.draw(surface)
        if self.mode == 5:
            self.shoot_group.draw(surface)

    def spawn_arrow(self):
        Arrow(self.x, self.y, 1, self.legs_group)  # todo разобраться

    def update(self):
        print("dsafdfs")
        cur_sprite = None
        self.legs.update()  # обновляем ноги
        if self.mode == 0:
            cur_sprite = self.body
            cur_sprite.cur_frame = self.legs.cur_frame
        if self.mode == 1:
            cur_sprite = self.body_sword_attack
            if self.prev_sheet > cur_sprite.cur_frame:
                self.prev_sheet = 0
                self.mode = 2
            else:
                self.prev_sheet = cur_sprite.cur_frame
        if self.mode == 2:
            cur_sprite = self.body_sword_run
            cur_sprite.cur_frame = self.legs.cur_frame % 5
        if self.mode == 3:
            cur_sprite = self.body_lamp_run
            cur_sprite.cur_frame = self.legs.cur_frame % 5

        if self.mode == 5:
            cur_sprite = self.body_shoot
            if self.prev_sheet > cur_sprite.cur_frame:
                self.prev_sheet = 0
                self.spawn_arrow()
                self.mode = 4
            else:
                self.prev_sheet = cur_sprite.cur_frame
        if self.mode == 4:
            cur_sprite = self.body_bow_run
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
    time = 0
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
                if event.key == pygame.K_5:
                    character.set_mode(4)
                if event.key == pygame.K_6:
                    character.set_mode(5)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    character.attack()

        screen.fill((0, 0, 0))
        character.draw(screen)
        if time >= 100:
            character.update()
            time = 0
        character.move(character.x + 1, character.y + 1)
        # стрелы спавнятся, но не летят, не знаю по чему
        time += clock.tick(60)
        pygame.display.flip()
    pygame.quit()
