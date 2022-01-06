import pygame
import random
from parameters import CELL_SIZE
from model.util import load_image
import model.value_manager
import view.level
import view.dungeon
import time


class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.f_x = self.rect.x
        self.f_y = self.rect.y

    # Положение на координатной оси верхнего левого края
    def get_dung_coords(self):
        return (self.f_x + 1) // CELL_SIZE, (self.f_y + 1) // CELL_SIZE

    # Положение на координатной оси нижнего правого края
    def get_d_dung_coords(self):
        return (self.f_x + self.rect.w - 1) // CELL_SIZE, (self.f_y + self.rect.h - 1) // CELL_SIZE


class Character(Creature):
    image = load_image('32x32_character.png')

    def __init__(self, x, y, *group):
        super().__init__(Character.image, x, y, *group)
        self.speed = 4
        self.lighting_area = 1
        self.move_data = [0, 0, 0, 0]
        self.prev_coord = None
        self.prev_d_coord = None
        self.path = [self.get_dung_coords()]
        self.prev_light_sprites = []
        # TODO загрузка из файла
        self.prev_light_time = -1

    def update(self, event):
        self.lighting_area = model.value_manager.ValueManager.light
        self.speed = model.value_manager.ValueManager.speed

        level = view.level.LevelManager.get_current_level()
        neighbours = level.dungeon.get_neighbours_coords(self, 0)
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_data[0] = 1
                elif event.key == pygame.K_RIGHT:
                    self.move_data[1] = 1
                elif event.key == pygame.K_DOWN:
                    self.move_data[2] = 1
                elif event.key == pygame.K_LEFT:
                    self.move_data[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.move_data[0] = 0
                elif event.key == pygame.K_RIGHT:
                    self.move_data[1] = 0
                elif event.key == pygame.K_DOWN:
                    self.move_data[2] = 0
                elif event.key == pygame.K_LEFT:
                    self.move_data[3] = 0

        if self.move_data[0] == 1:
            self.rect.y -= self.speed
            self.f_y -= self.speed
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.y += self.speed
            self.f_y += self.speed

        if self.move_data[1] == 1:
            self.rect.x += self.speed
            self.f_x += self.speed
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x -= self.speed
            self.f_x -= self.speed

        if self.move_data[2] == 1:
            self.rect.y += self.speed
            self.f_y += self.speed
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.y -= self.speed
            self.f_y -= self.speed

        if self.move_data[3] == 1:
            self.rect.x -= self.speed
            self.f_x -= self.speed
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x += self.speed
            self.f_x += self.speed

        coord = self.get_dung_coords()
        d_coord = self.get_d_dung_coords()
        if coord != self.prev_coord and self.path[-1] != coord:
            self.path.append(coord)
        elif d_coord != self.prev_d_coord and self.path[-1] != d_coord:
            self.path.append(d_coord)
        self.prev_coord = coord
        self.prev_d_coord = d_coord

        for sprite in self.prev_light_sprites:
            sprite.set_light(7)
        self.prev_light_sprites.clear()
        for ngh in level.dungeon.get_light_area(self, self.lighting_area):
            for sprite in ngh[0]:
                sprite.set_light(ngh[1])
                self.prev_light_sprites.append(sprite)

    def get_path(self):
        return self.path
    #
    # def update(self, light):
    #     current = time.time()
    #     if current - self.prev_light_time > 120:
    #         self.lighting_area = min(0, self.lighting_area - 1)
    #         self.prev_light_time = current


class Ghost(Creature):
    image = load_image('32x32_ghost.png')

    def __init__(self, x, y, *group):
        super().__init__(Ghost.image, x, y, *group)
        self.speed = 1
        self.see_radius = 5
        self.attacking = False
        self.attack_time = 4
        self.start_attack_moment = -1
        self.prev_direction = random.choice([1, 2, 3, 4])
        self.main_hero_pos_index = -1
        self.prev_point = None

    def update(self, event):
        level = view.level.LevelManager.get_current_level()
        character = level.character
        direction = self.prev_direction
        prev_pos = (self.rect.x, self.rect.y)
        cnt_speed = random.choice([2, 4, 6, 8, 16])
        if direction == 1:
            self.rect.y -= (self.speed + cnt_speed)
        elif direction == 2:
            self.rect.x += (self.speed + cnt_speed)
        elif direction == 3:
            self.rect.y += (self.speed + cnt_speed)
        elif direction == 4:
            self.rect.x -= (self.speed + cnt_speed)

        if self.attacking:
            self.clear_cnt_speed(direction, cnt_speed)
            if (time.time() - self.start_attack_moment) >= self.attack_time:
                self.end_attack()
            elif self.get_dung_coords() == self.get_d_dung_coords() \
                    and self.get_dung_coords() == character.get_path()[self.main_hero_pos_index]:
                path = character.get_path()
                dung_coords = self.get_dung_coords()
                self.main_hero_pos_index = min(self.main_hero_pos_index + 1, len(path) - 1)
                if path[self.main_hero_pos_index][1] < dung_coords[1]:
                    self.prev_direction = 1
                elif path[self.main_hero_pos_index][0] > dung_coords[0]:
                    self.prev_direction = 2
                elif path[self.main_hero_pos_index][1] > dung_coords[1]:
                    self.prev_direction = 3
                elif path[self.main_hero_pos_index][0] < dung_coords[0]:
                    self.prev_direction = 4
                else:
                    self.prev_direction = 0
            if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
                self.rect.x = prev_pos[0]
                self.rect.y = prev_pos[1]
        elif pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x = prev_pos[0]
            self.rect.y = prev_pos[1]
            if random.random() < 0.995:
                if direction in (1, 3):
                    self.prev_direction = random.choice((2, 4))
                else:
                    self.prev_direction = random.choice((1, 3))
        elif self.get_dung_coords() == self.get_d_dung_coords() != self.prev_point:
            self.prev_point = self.get_dung_coords()
            self.clear_cnt_speed(direction, cnt_speed)
            for k, v in level.dungeon.get_neighbours_coords(self, 1).items():
                if direction in (1, 3):
                    if k in (2, 4) and level.dungeon.get_object_at(*v[0]) == view.dungeon.NOTHING_SIGN:
                        if random.random() <= 0.5:
                            self.prev_direction = k
                if direction in (2, 4):
                    if k in (1, 3) and level.dungeon.get_object_at(*v[0]) == view.dungeon.NOTHING_SIGN:
                        if random.random() <= 0.5:
                            self.prev_direction = k
        else:
            self.clear_cnt_speed(direction, cnt_speed)
        self.f_x += (self.rect.x - prev_pos[0])
        self.f_y += (self.rect.y - prev_pos[1])
        if not self.attacking:
            neighbours = level.dungeon.get_neighbours_coords(self, self.see_radius)
            main_hero_coords = level.character.get_dung_coords()
            for coords in neighbours[direction]:
                if level.dungeon.get_object_at(*coords) == view.dungeon.WALL_SIGN:
                    break
                if main_hero_coords == coords:
                    self.start_attack()

    def start_attack(self):
        self.attacking = True
        self.start_attack_moment = time.time()
        self.main_hero_pos_index = len(view.level.LevelManager
                                       .get_current_level().character.get_path()) - 1
        self.speed *= 2

    def end_attack(self):
        self.attacking = False
        self.speed //= 2

    def clear_cnt_speed(self, direction, cnt_speed):
        if direction == 1:
            self.rect.y += cnt_speed
        elif direction == 2:
            self.rect.x -= cnt_speed
        elif direction == 3:
            self.rect.y -= cnt_speed
        elif direction == 4:
            self.rect.x += cnt_speed



