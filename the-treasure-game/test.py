import random
import pygame
from model.util import load_image

WALL_SIGN = "#"
NOTHING_SIGN = "."

wall_1_path = "64x64 wall_1.png"
floor_1_path = "64x64 floor_1.png"
cell_size = 64


class Dungeon:
    def __init__(self, size):
        self.data = self.generate(size)
        self.walls_sprite_group = pygame.sprite.Group()
        self.floor_sprite_group = pygame.sprite.Group()
        for row in range(len(self.data)):
            for col in range(len(self.data)):
                if self.data[row][col] == WALL_SIGN:
                    wall = Wall(self.walls_sprite_group)
                    wall.rect.x = row * cell_size
                    wall.rect.y = col * cell_size
                if self.data[row][col] == NOTHING_SIGN:
                    floor = Floor(self.floor_sprite_group)
                    floor.rect.x = row * cell_size
                    floor.rect.y = col * cell_size
        print(self.data)

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
        # print(row_pos_del, col_pos_del)

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

        # print(*list(map(lambda x: " ".join(x), data)), sep="\n", end="\n\n")
        if is_first:
            # print("first:")
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
            # print(rand)
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


class Wall(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image(wall_1_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image(floor_1_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    loop = True
    dungeon = Dungeon(5)

    fps = 30
    clock = pygame.time.Clock()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        screen.fill((0, 0, 0))
        dungeon.walls_sprite_group.draw(screen)
        dungeon.floor_sprite_group.draw(screen)

        clock.tick(fps)
        pygame.display.flip() # todo wall class

