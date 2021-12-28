import pygame
import random
from game.view.object_sprites import Floor1
from game.view.object_sprites import Wall1

WALL_SIGN = "#"
NOTHING_SIGN = "."

cell_size = 64

class Dungeon:
    def __init__(self, size):
        self.data = self.generate(size)
        self.walls_sprite_group = pygame.sprite.Group()
        self.floor_sprite_group = pygame.sprite.Group()
        self.character_sprite_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.draw_dungeon()

    def draw_dungeon(self):
        for col in range(0, len(self.data) + 2):
            Wall1(col * cell_size, 0, self.walls_sprite_group, self.all_sprites)
        for row in range(1, len(self.data) + 1):
            Wall1(0, row * cell_size, self.walls_sprite_group, self.all_sprites)
            for col in range(1, len(self.data) + 1):
                if self.data[row - 1][col - 1] == WALL_SIGN:
                    Wall1(col * cell_size, row * cell_size, self.walls_sprite_group, self.all_sprites)
                if self.data[row - 1][col - 1] == NOTHING_SIGN:
                    Floor1(col * cell_size, row * cell_size, self.floor_sprite_group, self.all_sprites)
            Wall1((len(self.data) + 1) * cell_size, row * cell_size, self.walls_sprite_group, self.all_sprites)
        for col in range(0, len(self.data) + 2):
            Wall1(col * cell_size, (len(self.data) + 1) * cell_size, self.walls_sprite_group, self.all_sprites)

    def randomize_ways(self, data, row, col):
        row_pos_del = 0
        col_pos_del = 0
        result = [1, 2, 3, 4]  # 1 - вверх 2 - вправо 3 - вниз 4 - влево
        # когда переменная равна 1, значит по координате позиция находится в максимальном положении
        # -1 - в минимальном
        if row == 0:
            row_pos_del = -1
            result.remove(1)
        elif row == len(data) - 1:
            row_pos_del = 1
            result.remove(3)
        if col == 0:
            col_pos_del = -1
            result.remove(4)
        elif col == len(data) - 1:
            col_pos_del = 1
            result.remove(2)

        # проверяем верх (1)
        if row_pos_del != -1:
            if data[row - 2][col] == NOTHING_SIGN:
                result.remove(1)
        # проверяем низ (3)
        if row_pos_del != 1:
            if data[row + 2][col] == NOTHING_SIGN:
                result.remove(3)
        # проверяем право (2)
        if col_pos_del != 1:
            if data[row][col + 2] == NOTHING_SIGN:
                result.remove(2)
        # проверяем лево (4)
        if col_pos_del != -1:
            if data[row][col - 2] == NOTHING_SIGN:
                result.remove(4)
        if len(result) == 0:
            rcresult = 0
        else:
            rcresult = random.choice(result)

        if rcresult == 0:
            return 0, 0
        if rcresult == 1:
            return -1, 0
        if rcresult == 2:
            return 0, 1
        if rcresult == 3:
            return 1, 0
        if rcresult == 4:
            return 0, -1

    def generate(self, dots_num, is_first=True, row=0, col=0, pos_data=None, data=None):
        if data is None:
            data = []
        if pos_data is None:
            pos_data = []

        if is_first:
            is_first = False
            data = [[WALL_SIGN for i in range(dots_num * 2 - 1)] for j in range(dots_num * 2 - 1)]
            dots_num = dots_num * dots_num - 1
            data[row][col] = NOTHING_SIGN
            pos_data.append((row, col))
            return self.generate(dots_num, is_first, row, col, pos_data, data)
        elif dots_num == 0:
            return data
        else:
            rand = self.randomize_ways(data, row, col)
            if rand == (0, 0):
                # back step
                cords = pos_data.pop(-1)
                return self.generate(dots_num, is_first, cords[0], cords[1], pos_data, data)
            data[row + rand[0]][col + rand[1]] = NOTHING_SIGN
            row = row + rand[0] * 2
            col = col + rand[1] * 2
            data[row][col] = NOTHING_SIGN
            dots_num -= 1
            pos_data.append((row, col))
            return self.generate(dots_num, is_first, row, col, pos_data, data)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, direction=None):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, width, height):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)