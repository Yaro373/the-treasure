import pygame
import random
from view.object_sprites import Floor1
from view.object_sprites import Wall1, UnbreakableWall, Chest
import view.creature
from parameters import CELL_SIZE

NOTHING_SIGN = 0
WALL_SIGN = 1
GHOST_SIGN = 2
CHEST_SIGN = 3
UNBREAKABLE_WALL_SIGN = 4


class Dungeon:
    def __init__(self, size):
        self.data = DungeonGenerator.generate(size)
        self.walls_sprite_group = pygame.sprite.Group()
        self.floor_sprite_group = pygame.sprite.Group()
        self.character_sprite_group = pygame.sprite.Group()
        self.ghost_sprite_group = pygame.sprite.Group()
        self.chest_sprite_group = pygame.sprite.Group()
        self.item_sprite_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.sprites_matrix = [[[0] for i in range(len(self.data))] for j in range(len(self.data))]
        self.draw_dungeon()

    def draw_dungeon(self):
        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                if self.data[row][col] == WALL_SIGN:
                    Wall1(row * CELL_SIZE, col * CELL_SIZE, self.walls_sprite_group,
                          self.all_sprites)
                elif self.data[row][col] == UNBREAKABLE_WALL_SIGN:
                    UnbreakableWall(row * CELL_SIZE, col * CELL_SIZE, self.walls_sprite_group,
                                    self.all_sprites)
                else:
                    Floor1(row * CELL_SIZE, col * CELL_SIZE, self.floor_sprite_group,
                           self.all_sprites)
        Chest(3 * CELL_SIZE, 3 * CELL_SIZE, self.chest_sprite_group, self.all_sprites)

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

    def get_sprite_at(self, x, y):
        return self.sprites_matrix[x][y]


class DungeonGenerator:
    @staticmethod
    def generate(n):
        stek = [(1, 1)]  # список посещенных клеток
        result = [[WALL_SIGN for i in range(n * 2 + 1)] for i in
                  range(n * 2 + 1)]  # подземелье в виде матрицы
        unvisited_cells_num = n * n - 1  # количество непосещенных клеток
        visited = [(1, 1)]  # список со всеми посещенными клетками
        current_cell = 1, 1  # текущие координаты
        result[1][1] = NOTHING_SIGN
        # окружаем поле неразрушимыми стенами
        for i in range(len(result)):
            if i == 0 or i == len(result) - 1:
                for j in range(len(result)):
                    result[i][j] = UNBREAKABLE_WALL_SIGN
            else:
                result[i][0] = UNBREAKABLE_WALL_SIGN
                result[i][-1] = UNBREAKABLE_WALL_SIGN
        # прокладываем дороги
        while unvisited_cells_num > 0:
            # проверяем, есть ли не посещенные соседи
            unvisited_cells = []
            # слева 1
            if current_cell[1] > 1 and (current_cell[0], current_cell[1] - 2) not in visited:
                unvisited_cells.append(1)
            # вверх 2
            if current_cell[0] > 1 and (current_cell[0] - 2, current_cell[1]) not in visited:
                unvisited_cells.append(2)
            # справа 3
            if current_cell[1] < len(result) - 2 and \
                    (current_cell[0], current_cell[1] + 2) not in visited:
                unvisited_cells.append(3)
            # снизу 4
            if current_cell[0] < len(result) - 2 and \
                    (current_cell[0] + 2, current_cell[1]) not in visited:
                unvisited_cells.append(4)
            # если у точки есть непосещенные соседи

            if len(unvisited_cells) > 0:
                # перемещаемся
                choise = random.choice(unvisited_cells)
                stek.append(current_cell)
                if choise == 1:  # влево
                    result[current_cell[0]][current_cell[1] - 2] = NOTHING_SIGN
                    result[current_cell[0]][current_cell[1] - 1] = NOTHING_SIGN
                    current_cell = current_cell[0], current_cell[1] - 2
                if choise == 2:  # верх
                    result[current_cell[0] - 1][current_cell[1]] = NOTHING_SIGN
                    result[current_cell[0] - 2][current_cell[1]] = NOTHING_SIGN
                    current_cell = current_cell[0] - 2, current_cell[1]
                if choise == 3:  # справа
                    result[current_cell[0]][current_cell[1] + 2] = NOTHING_SIGN
                    result[current_cell[0]][current_cell[1] + 1] = NOTHING_SIGN
                    current_cell = current_cell[0], current_cell[1] + 2
                if choise == 4:  # снизу
                    result[current_cell[0] + 1][current_cell[1]] = NOTHING_SIGN
                    result[current_cell[0] + 2][current_cell[1]] = NOTHING_SIGN
                    current_cell = current_cell[0] + 2, current_cell[1]
            # иначе
            else:
                current_cell = stek.pop(-1)
            if current_cell not in visited:
                visited.append(current_cell)
                unvisited_cells_num -= 1

        return result


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
