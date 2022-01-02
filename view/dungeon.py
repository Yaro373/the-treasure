import pygame
import random
from view.object_sprites import Floor1
from view.object_sprites import Wall1
import view.creature
from parameters import CELL_SIZE

NOTHING_SIGN = 0
WALL_SIGN = 1
GHOST_SIGN = 2


class Dungeon:
    def __init__(self, size):
        self.data = DungeonGenerator.generate(size)
        self.walls_sprite_group = pygame.sprite.Group()
        self.floor_sprite_group = pygame.sprite.Group()
        self.character_sprite_group = pygame.sprite.Group()
        self.ghost_sprite_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.draw_dungeon()

    def draw_dungeon(self):
        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                if self.data[row][col] == WALL_SIGN:
                    Wall1(row * CELL_SIZE, col * CELL_SIZE, self.walls_sprite_group,
                          self.all_sprites)
                else:
                    Floor1(row * CELL_SIZE, col * CELL_SIZE, self.floor_sprite_group,
                           self.all_sprites)

    def get_creature_sprite_neighbours(self, sprite, radius):
        x, y = sprite.get_dung_coords()
        left_x = max(x - radius, 0)
        right_x = min(x + radius, len(self.data) - 1)
        up_y = max(y - radius, 0)
        down_y = min(y + radius, len(self.data) - 1)
        result = {0: [], 1: [], 2: [], 3: [], 4: []}
        result[0].append((x, y))
        for i in range(max(0, y - 1), up_y - 1, -1):
            result[1].append((x, i))
        for i in range(min(len(self.data) - 1, y + 1), down_y + 1):
            result[3].append((x, i))
        for i in range(max(0, x - 1), left_x - 1, -1):
            result[4].append((i, y))
        for i in range(min(len(self.data) - 1, x + 1), right_x + 1):
            result[2].append((i, y))
        return result

    def get_object_at(self, x, y):
        return self.data[x][y]


class DungeonGenerator:
    @staticmethod
    def randomize_ways(data, row, col):
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

    @staticmethod
    def generate(dots_num, is_first=True, row=0, col=0, pos_data=None, data=None):
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
            return DungeonGenerator.generate(dots_num, is_first, row, col, pos_data, data)
        elif dots_num == 0:
            return data
        else:
            rand = DungeonGenerator.randomize_ways(data, row, col)
            if rand == (0, 0):
                # back step
                cords = pos_data.pop(-1)
                return DungeonGenerator.generate(dots_num, is_first, cords[0], cords[1], pos_data, data)
            data[row + rand[0]][col + rand[1]] = NOTHING_SIGN
            row = row + rand[0] * 2
            col = col + rand[1] * 2
            data[row][col] = NOTHING_SIGN
            dots_num -= 1
            pos_data.append((row, col))
            return DungeonGenerator.generate(dots_num, is_first, row, col, pos_data, data)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, width, height):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
