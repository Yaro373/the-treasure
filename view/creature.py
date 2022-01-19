import pygame
import random
from parameters import CELL_SIZE
from model.util import load_image, seconds_to_milliseconds
from view.util_sprites import Arrow, GhostBall
import model.value_manager
import view.level
import view.dungeon
import time


class PathIncorrectLoopException(Exception):
    pass


class BaseCharacteristics:
    def __init__(self, health, speed, fire_interval, harm):
        self.health = health
        self.speed = speed
        self.fire_interval = fire_interval
        self.harm = harm


class GhostCharacteristics:
    def __init__(self, base_characteristics, see_radius, attack_time):
        self.base_characteristics = base_characteristics
        self.see_radius = see_radius
        self.attack_time = attack_time
        self.fire_speed = base_characteristics.speed + 10


class Creature(pygame.sprite.Sprite):
    def __init__(self, image, x, y, characteristics, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.f_x = self.rect.x
        self.f_y = self.rect.y

        self.health = characteristics.health
        self.speed = characteristics.speed
        self.fire_interval = characteristics.fire_interval
        self.harm = characteristics.harm

        self.current_speed = self.speed

        self.fire_moment = -1

    # Положение на координатной оси верхнего левого края
    def get_dung_coords(self, deviation=0):
        return (self.f_x + 1 - deviation) // CELL_SIZE, (self.f_y + 1 - deviation) // CELL_SIZE

    # Положение на координатной оси нижнего правого края
    def get_d_dung_coords(self, deviation=0):
        return (self.f_x + self.rect.w - 1 - deviation) // CELL_SIZE, \
               (self.f_y + self.rect.h - 1 - deviation) // CELL_SIZE

    def correct_health(self, health):
        self.health += health

    def set_fire_moment(self):
        self.fire_moment = pygame.time.get_ticks()

    def can_fire(self):
        if self.fire_moment == -1:
            return True
        return pygame.time.get_ticks() - self.fire_moment >= self.fire_interval

    def update(self, event):
        if self.health == 0:
            self.kill()


class Character(Creature):
    image = load_image('32x32_character.png')
    invisibility_image = image.copy()
    invisibility_image.set_alpha(50)

    characteristics = BaseCharacteristics(100, 2, 250, 15)

    def __init__(self, x, y, items, *group):
        super().__init__(Character.image, x, y, Character.characteristics, *group)
        self.speed = 4
        self.hearing_area_size = 5
        self.lighting_area = 1
        self.hearing_area = set()
        self.direction = 1
        self.move_data = [0, 0, 0, 0]
        self.prev_coord = None
        self.prev_d_coord = None
        self.path = [self.get_dung_coords()]
        self.prev_light_sprites = []
        self.items = items
        self.logging = False
        # TODO загрузка из файла
        self.remain = seconds_to_milliseconds(60)
        self.start = pygame.time.get_ticks()

    def fire(self, *group):
        if self.can_fire():
            self.set_fire_moment()
            x, y = self.rect.x, self.rect.y
            Arrow(x + self.rect.w // 2, y + self.rect.h // 2, self.direction, *group)

    def set_visibility(self, visibility):
        if visibility:
            self.image = Character.image
        else:
            self.image = Character.invisibility_image

    def update(self, event):
        super().update(event)

        if len(self.items) < (size := model.value_manager.ValueManager.inventory_size):
            self.items += [None] * (size - len(self.items))
            view.level.LevelManager.get_current_level().reload_main_inventory()
        if len(self.items) > (size := model.value_manager.ValueManager.inventory_size):
            self.items = self.items[:size]
            view.level.LevelManager.get_current_level().reload_main_inventory()

        self.__update_light()
        self.lighting_area = model.value_manager.ValueManager.light
        self.speed = model.value_manager.ValueManager.speed

        level = view.level.LevelManager.get_current_level()
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_data[0] = 1
                elif event.key == pygame.K_d:
                    self.move_data[1] = 1
                elif event.key == pygame.K_s:
                    self.move_data[2] = 1
                elif event.key == pygame.K_a:
                    self.move_data[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_data[0] = 0
                elif event.key == pygame.K_d:
                    self.move_data[1] = 0
                elif event.key == pygame.K_s:
                    self.move_data[2] = 0
                elif event.key == pygame.K_a:
                    self.move_data[3] = 0

        if self.move_data[0] == 1:
            self.rect.y -= self.speed
            self.f_y -= self.speed
            self.direction = 1
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.y += self.speed
            self.f_y += self.speed

        if self.move_data[1] == 1:
            self.rect.x += self.speed
            self.f_x += self.speed
            self.direction = 2
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x -= self.speed
            self.f_x -= self.speed

        if self.move_data[2] == 1:
            self.rect.y += self.speed
            self.f_y += self.speed
            self.direction = 3
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.y -= self.speed
            self.f_y -= self.speed

        if self.move_data[3] == 1:
            self.rect.x -= self.speed
            self.f_x -= self.speed
            self.direction = 4
        if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x += self.speed
            self.f_x += self.speed

        if self.logging:
            coord = self.get_dung_coords()
            d_coord = self.get_d_dung_coords()
            if len(self.path) == 0 or (coord != self.prev_coord and self.path[-1] != coord):
                self.path.append(coord)
            elif len(self.path) == 0 or (d_coord != self.prev_d_coord and self.path[-1] != d_coord):
                self.path.append(d_coord)
            self.prev_coord = coord
            self.prev_d_coord = d_coord

        self.hearing_area = view.level.LevelManager.get_current_level().dungeon\
            .get_radius_neighbours_coords(self.hearing_area_size)
        self.__make_light(level)

    def get_hearing_area(self):
        return self.hearing_area

    def start_log(self):
        self.path.clear()
        self.path = [self.get_dung_coords()]
        self.logging = True

    def end_log(self):
        self.logging = False

    def get_path(self):
        return self.path

    def correct_health(self, health):
        model.value_manager.ValueManager.update_health(health)

    def remove_path_loops(self):
        i = 0
        while i < len(self.path):
            el = self.path[i]
            if self.path.count(el) > 1:
                if self.path.count(el) % 2 == 1:
                    self.path = [self.path[-1]]
                    raise PathIncorrectLoopException
                self.path.pop(i)
                self.path = self.path[:i] + self.path[self.path.index(el):]
            i += 1

    def __update_light(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start > self.remain:
            model.value_manager.ValueManager.update_light(-1)
            self.start = current_time
            self.remain = seconds_to_milliseconds(60)

    def __make_light(self, level):
        for sprite in self.prev_light_sprites:
            sprite.set_light(7)
        self.prev_light_sprites.clear()
        for ngh in level.dungeon.get_light_area(self.lighting_area):
            for sprite in ngh[0]:
                sprite.set_light(ngh[1])
                self.prev_light_sprites.append(sprite)


class Ghost(Creature):
    image = load_image('32x32_ghost.png')
    not_visible_image = image.copy()
    not_visible_image.set_alpha(0)

    def __init__(self, x, y, level, *group):
        data = GhostDataManager.get_data_by_level(level)

        super().__init__(Ghost.image, x, y, data.characteristics.base_characteristics, *group)
        self.see_radius = data.characteristics.see_radius
        self.attack_time = data.characteristics.attack_time
        self.fire_speed = data.characteristics.fire_speed
        self.image = data.image

        self.attacking = False
        self.start_attack_moment = -1
        self.direction = random.choice([1, 2, 3, 4])
        self.main_hero_pos_index = -1
        self.prev_point = None

    def update(self, event):
        super().update(event)
        level = view.level.LevelManager.get_current_level()
        character = level.character
        direction = self.direction
        prev_pos = (self.rect.x, self.rect.y)
        cnt_speed = random.choice([2, 4, 6, 8, 16])
        if direction == 1:
            self.rect.y -= (self.current_speed + cnt_speed)
        elif direction == 2:
            self.rect.x += (self.current_speed + cnt_speed)
        elif direction == 3:
            self.rect.y += (self.current_speed + cnt_speed)
        elif direction == 4:
            self.rect.x -= (self.current_speed + cnt_speed)

        # TODO dev
        dev = 0
        if self.attacking:
            self.__clear_cnt_speed(direction, cnt_speed)
            if not self.can_attack():
                self.end_attack()
                character.end_log()
            elif (time.time() - self.start_attack_moment) >= self.attack_time:
                self.end_attack()
                character.end_log()
            elif self.get_dung_coords(dev) == self.get_d_dung_coords(dev) \
                    and self.get_dung_coords(dev) == character.get_path()[0]:
                dung_coords = self.get_dung_coords(dev)
                d_dung_coords = self.get_d_dung_coords(dev)

                if len(character.path) > 1:
                    character.path.pop(0)
                try:
                    character.remove_path_loops()
                    path = character.get_path()
                    if path[0] == dung_coords or path[0] == d_dung_coords:
                        self.direction = 0
                    elif path[0][1] < dung_coords[1]:
                        self.direction = 1
                    elif path[0][0] > dung_coords[0]:
                        self.direction = 2
                    elif path[0][1] > dung_coords[1]:
                        self.direction = 3
                    elif path[0][0] < dung_coords[0]:
                        self.direction = 4
                except PathIncorrectLoopException:
                    self.end_attack()

            if pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
                self.rect.x = prev_pos[0]
                self.rect.y = prev_pos[1]
                self.end_attack()
        elif pygame.sprite.spritecollideany(self, level.dungeon.walls_sprite_group):
            self.rect.x = prev_pos[0]
            self.rect.y = prev_pos[1]
            if random.random() < 0.995:
                if direction in (1, 3):
                    self.direction = random.choice((2, 4))
                else:
                    self.direction = random.choice((1, 3))
        elif self.get_dung_coords(dev) == self.get_d_dung_coords(dev) != self.prev_point:
            self.prev_point = self.get_dung_coords(dev)
            self.__clear_cnt_speed(direction, cnt_speed)
            for k, v in level.dungeon.get_neighbours_coords(self.get_dung_coords(8), 1).items():
                if direction in (1, 3):
                    if k in (2, 4) and level.dungeon.get_object_at(*v[0]) == view.dungeon.NOTHING_SIGN:
                        if random.random() <= 0.5:
                            self.direction = k
                if direction in (2, 4):
                    if k in (1, 3) and level.dungeon.get_object_at(*v[0]) == view.dungeon.NOTHING_SIGN:
                        if random.random() <= 0.5:
                            self.direction = k
        else:
            self.__clear_cnt_speed(direction, cnt_speed)
        self.f_x += (self.rect.x - prev_pos[0])
        self.f_y += (self.rect.y - prev_pos[1])
        if not self.attacking:
            neighbours = level.dungeon.get_neighbours_coords(self.get_dung_coords(), self.see_radius)
            main_hero_coords = level.character.get_dung_coords()
            for coords in neighbours[direction] + neighbours[0]:
                if level.dungeon.get_object_at(*coords) == view.dungeon.WALL_SIGN:
                    break
                if main_hero_coords == coords and self.can_attack():
                    self.start_attack()
                    character.start_log()

        if self.health <= 0:
            self.kill()

    def set_not_visible(self):
        self.image = Ghost.not_visible_image

    def set_visible(self):
        self.image = Ghost.image

    def fire(self, *group):
        level = view.level.LevelManager.get_current_level()
        if self.attacking and self.can_fire():
            x, y = self.get_dung_coords()
            cx, cy = level.character.get_dung_coords()
            if self.direction in (2, 4) and abs(x - cx) <= 5 and y == cy:
                GhostBall(self.rect.x, self.rect.y, self.direction, self.fire_speed, self.harm, *group)
            if self.direction in (1, 3) and abs(y - cy) <= 5 and x == cx:
                GhostBall(self.rect.x,
                          self.rect.y, self.direction, self.fire_speed, self.harm, *group)
            self.set_fire_moment()

    def can_attack(self):
        return model.value_manager.ValueManager.is_visibility()

    def start_attack(self):
        self.attacking = True
        self.start_attack_moment = time.time()
        self.main_hero_pos_index = len(view.level.LevelManager
                                       .get_current_level().character.get_path()) - 1
        self.current_speed = self.speed * 2

    def end_attack(self):
        self.attacking = False
        self.direction = random.choice([1, 2, 3, 4])
        self.current_speed = self.speed

    def __clear_cnt_speed(self, direction, cnt_speed):
        if direction == 1:
            self.rect.y += cnt_speed
        elif direction == 2:
            self.rect.x -= cnt_speed
        elif direction == 3:
            self.rect.y -= cnt_speed
        elif direction == 4:
            self.rect.x += cnt_speed


class GhostData:
    def __init__(self, characteristics, image):
        self.characteristics = characteristics
        self.image = image


class GhostDataManager:
    @staticmethod
    def get_data_by_level(level):
        characteristics = GhostCharacteristicsManager.get_characteristics_by_level(level)
        data = GhostImageManager.get_image_by_level(level)
        return GhostData(characteristics, data)


class GhostCharacteristicsManager:
    __data = {
        1: GhostCharacteristics(BaseCharacteristics(30, 1, 5000, 10), 5, 15),
        2: GhostCharacteristics(BaseCharacteristics(60, 2, 3000, 20), 7, 30),
        3: GhostCharacteristics(BaseCharacteristics(100, 3, 1000, 35), 9, 45),
    }

    @staticmethod
    def get_characteristics_by_level(level):
        return GhostCharacteristicsManager.__data[level]


class GhostImageManager:
    __data = {
        1: load_image('32x32_ghost.png'),
        2: load_image('32x32_ghost.png'),
        3: load_image('32x32_ghost.png'),
    }

    @staticmethod
    def get_image_by_level(level):
        return GhostImageManager.__data[level]
