import random
import pygame
from game.model.util import load_image
from game.view.floor import Floor1
from game.view.floor import Floor2
from game.view.floor import Floor3
from game.view.wall import Wall1
from game.view.wall import Wall2
from game.view.wall import Wall3
import game.view.сharacter

WALL_SIGN = "#"
NOTHING_SIGN = "."

wall_1_path = "64x64_wall_1.png"
floor_1_path = "64x64_floor_1.png"
cell_size = 64

walls_sprite_group = pygame.sprite.Group()
floor_sprite_group = pygame.sprite.Group()
character_sprite_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Dungeon:
    def __init__(self, size):
        self.data = self.generate(size)
        for row in range(len(self.data)):
            for col in range(len(self.data)):
                if self.data[row][col] == WALL_SIGN:
                    Wall1(row * cell_size, col * cell_size, walls_sprite_group, all_sprites)
                if self.data[row][col] == NOTHING_SIGN:
                    Floor1(row * cell_size, col * cell_size, floor_sprite_group, all_sprites)

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

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    loop = True
    dungeon = Dungeon(4)
    camera = Camera()
    character = game.view.сharacter.Character(0, 0, character_sprite_group, all_sprites)

    fps = 60
    clock = pygame.time.Clock()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                character_sprite_group.update(event, walls_sprite_group)
            if event.type == pygame.KEYUP:
                character_sprite_group.update(event, walls_sprite_group)
        character_sprite_group.update(None, walls_sprite_group)
        for sprite in all_sprites:
            camera.apply(sprite)

        camera.update(character)
        screen.fill((0, 0, 0))
        walls_sprite_group.draw(screen)
        floor_sprite_group.draw(screen)
        character_sprite_group.draw(screen)

        clock.tick(fps)
        pygame.display.flip() # todo wall class

