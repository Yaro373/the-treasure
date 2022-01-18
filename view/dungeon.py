import pygame
import random
from view.object_sprites import Floor1
from view.object_sprites import Wall1, UnbreakableWall, Chest
from view.util_sprites import Arrow, GhostBall
import view.level
import view.creature
import model.tip
import resources.strings
from parameters import CELL_SIZE

NOTHING_SIGN = 0
WALL_SIGN = 1
GHOST_SIGN = 2
CHEST_SIGN = 3
UNBREAKABLE_WALL_SIGN = 4
FAKE_STATUE_SIGN = 5


class Dungeon:
    def __init__(self, data, wall_sprite, floor_sprite, chests_inventory=None, enemies_positions=None):
        self.data = data
        self.wall_sprite = wall_sprite
        self.floor_sprite = floor_sprite
        self.chests_inventory = chests_inventory
        self.enemies_positions = enemies_positions
        self.walls_sprite_group = pygame.sprite.Group()
        self.floor_sprite_group = pygame.sprite.Group()
        self.character_sprite_group = pygame.sprite.Group()
        self.ghost_sprite_group = pygame.sprite.Group()
        self.chest_sprite_group = pygame.sprite.Group()
        self.item_sprite_group = pygame.sprite.Group()
        self.weapon_sprite_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.sprites_matrix = [[[0] for i in range(len(self.data))] for j in range(len(self.data))]
        self.draw_dungeon()

    def draw_dungeon(self):
        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                if self.data[row][col] == WALL_SIGN:
                    wall1 = self.wall_sprite(row * CELL_SIZE, col * CELL_SIZE, self.walls_sprite_group,
                           self.all_sprites)
                    self.sprites_matrix[row][col] = (wall1, )

                elif self.data[row][col] == UNBREAKABLE_WALL_SIGN:
                    uwall = UnbreakableWall(row * CELL_SIZE, col * CELL_SIZE,
                                            self.walls_sprite_group, self.all_sprites)

                    self.sprites_matrix[row][col] = (uwall, )

                elif self.data[row][col] == CHEST_SIGN:
                    floor1 = self.floor_sprite(row * CELL_SIZE, col * CELL_SIZE, self.floor_sprite_group,
                                    self.all_sprites)
                    if self.chests_inventory is not None and (row, col) in self.chests_inventory.keys():
                        chest = Chest(row * CELL_SIZE, col * CELL_SIZE, False,
                                      self.chest_sprite_group, self.all_sprites,
                                      items=self.chests_inventory[(row, col)][1])
                    else:
                        chest = Chest(row * CELL_SIZE, col * CELL_SIZE, False,
                                      self.chest_sprite_group,
                                      self.all_sprites, items=None)
                    self.sprites_matrix[row][col] = (floor1, chest, )

                else:
                    floor1 = self.floor_sprite(row * CELL_SIZE, col * CELL_SIZE, self.floor_sprite_group,
                           self.all_sprites)

                    self.sprites_matrix[row][col] = (floor1, )
        view.creature.Ghost(3 * CELL_SIZE, 3 * CELL_SIZE, 3, self.ghost_sprite_group,
                            self.all_sprites)
        if self.enemies_positions is not None:
            for pos in self.enemies_positions:
                view.creature.Ghost(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, self.ghost_sprite_group, self.all_sprites)

    def update(self, event):
        level = view.level.LevelManager.get_current_level()
        if event is not None:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                level.character.fire(self.weapon_sprite_group, self.all_sprites)
        for ghost in self.ghost_sprite_group:
            ghost.fire(self.weapon_sprite_group, self.all_sprites)

        dc = level.character.get_dung_coords()
        ddc = level.character.get_d_dung_coords()
        end_coords = (len(self.data) - 2, len(self.data) - 2)
        if dc == end_coords or ddc == end_coords:
            model.tip.TipManager.create_tip(resources.strings.end_level,
                                            while_coord=(len(self.data) - 2, len(self.data) - 2))

    def get_neighbours_coords(self, coords, radius):
        x, y = coords
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

    def get_radius_neighbours_coords(self, radius):
        x, y = view.level.LevelManager.get_current_level().character.get_dung_coords()
        wave = {(x, y)}
        for i in range(radius):
            next_wave = set()
            for el in wave:
                neighbours = self.get_neighbours_coords(el, 1)
                for k, v in neighbours.items():
                    for sel in v:
                        if sel not in wave:
                            next_wave.add(sel)
                    next_wave.update(set(v))
            wave.update(next_wave)
            next_wave.clear()
        return wave

    def get_light_area(self, radius):
        x, y = view.level.LevelManager.get_current_level().character.get_dung_coords()
        wave = {(x, y)}
        result = {((x, y), 7 - radius)}
        for i in range(radius):
            next_wave = set()
            for el in wave:
                if self.data[el[0]][el[1]] in (WALL_SIGN, UNBREAKABLE_WALL_SIGN):
                    continue
                neighbours = self.get_neighbours_coords(el, 1)
                for k, v in neighbours.items():
                    for sel in v:
                        if sel not in wave:
                            next_wave.add(sel)
                            result.add((sel, 7 - radius + i))
                    next_wave.update(set(v))
            wave.update(next_wave)
            next_wave.clear()
        result = [(self.sprites_matrix[coord[0]][coord[1]], degree) for coord, degree in result]
        return result

    def get_object_at(self, x, y):
        return self.data[x][y]

    def get_sprite_at(self, x, y):
        return self.sprites_matrix[x][y]

    def kill(self):
        for sprite in self.all_sprites:
            sprite.kill()


class DungeonGenerator:
    @staticmethod
    def generate(size):
        n = size
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
        # добавляем комнаты
        visited, unvisited_cells_num, result = DungeonGenerator.add_chests(result, size, visited,
                                                                           unvisited_cells_num)
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
                # перемещяемся
                choise = random.choice(unvisited_cells)
                stek.append(current_cell)
                if choise == 1:  # лево
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

    @staticmethod
    def add_chests(result, size, visited, unvisited_cells_num):
        """
        Добавляет комнаты с сундуками в подземелье.
        """
        res_visited = list(
            map(lambda x: ((x[0] - 1) // 2, (x[1] - 1) // 2), visited))  # преобразуем visited

        # создаем матрицу для выбора
        choice_data = []
        for x in range(size - 2):
            choice_data.append([(x, y) for y in range(size - 2)])
        print("choice_data:", choice_data)
        # удаляем ненужное
        for x, y in res_visited:
            choice_data[x][y] = None
        # обьединяем в один списко
        res_choice_data = []
        for i in choice_data:
            for el in i:
                if el != None:
                    res_choice_data.append(el)
        print("res_choice_data:", res_choice_data)

        # создаем комнату
        x, y = random.choice(res_choice_data)
        x *= 2
        x += 1
        y *= 2
        y += 1
        result[x][y] = NOTHING_SIGN  # лево верх
        visited.append((x, y))
        result[x + 1][y] = NOTHING_SIGN  # верх
        result[x + 2][y] = NOTHING_SIGN  # право верх
        visited.append((x + 2, y))
        result[x + 2][y + 1] = NOTHING_SIGN  # право
        result[x + 2][y + 2] = NOTHING_SIGN  # право низ
        visited.append((x + 2, y + 2))
        result[x + 1][y + 2] = NOTHING_SIGN  # низ
        result[x][y + 2] = NOTHING_SIGN  # лево низ
        visited.append((x, y + 2))
        result[x][y + 1] = NOTHING_SIGN  # лево
        result[x + 1][y + 1] = CHEST_SIGN  # центр
        unvisited_cells_num -= 4
        # добавляем проход в комнату
        choice_data = []  # 1 - лево, 2 - верх, 3 - право, 4 - низ
        if result[x - 1][y + 1] != UNBREAKABLE_WALL_SIGN:  # 1
            choice_data.append(1)
        if result[x + 1][y - 1] != UNBREAKABLE_WALL_SIGN:
            choice_data.append(2)
        if result[x + 3][y + 1] != UNBREAKABLE_WALL_SIGN:
            choice_data.append(3)
        if result[x + 1][y + 3] != UNBREAKABLE_WALL_SIGN:
            choice_data.append(4)

        choice = random.choice(choice_data)  # 1 - лево, 2 - верх, 3 - право, 4 - низ
        if choice == 1:
            result[x - 1][y + 1] = NOTHING_SIGN
            result[x - 2][y + 1] = NOTHING_SIGN
        if choice == 2:
            result[x + 1][y - 1] = NOTHING_SIGN
            result[x + 1][y - 2] = NOTHING_SIGN
        if choice == 3:
            result[x + 3][y + 1] = NOTHING_SIGN
            result[x + 4][y + 1] = NOTHING_SIGN
        if choice == 4:
            result[x + 1][y + 3] = NOTHING_SIGN
            result[x + 1][y + 4] = NOTHING_SIGN

        return visited, unvisited_cells_num, result


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
