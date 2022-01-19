import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('resources\\sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    loop = True
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    # тут уже просто лень было
    ghost = AnimatedSprite(load_image("128_128_ghost_1_animation.png"), 6, 1, 0, 0, all_sprites)
    ghost_05 = AnimatedSprite(load_image("128x128_ghost_1_get_damage.png"), 1, 1, 150, 0, all_sprites)
    ghost_1 = AnimatedSprite(load_image("128_128_ghost_2_animation.png"), 6, 1, 300, 0, all_sprites)
    ghost_15 = AnimatedSprite(load_image("128x128_ghost_2_get_damage.png"), 1, 1, 450, 0, all_sprites)
    ghost_2 = AnimatedSprite(load_image("128_128_ghost_3_animation.png"), 6, 1, 600, 0, all_sprites)
    ghost_25 = AnimatedSprite(load_image("128x128_ghost_3_get_damage.png"), 1, 1, 750, 0, all_sprites)
    time = 0
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                pass

        screen.fill((0, 0, 0))
        all_sprites.draw(surface=screen)
        if time >= 100:
            all_sprites.update()
            time = 0
        # стрелы спавнятся, но не летят, не знаю по чему
        time += clock.tick(60)
        pygame.display.flip()
    pygame.quit()