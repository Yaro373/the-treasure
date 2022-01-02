import pygame
import csv
import os.path
import view.level
from parameters import GAME_TITLE


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_TITLE)
    level_manager = view.level.LevelManager()
    level = level_manager.get_current_level()

    health_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_health.png'))
    hearing_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_hearing.png'))
    speed_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_speed.png'))

    loop = True

    fps = 60
    clock = pygame.time.Clock()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                level.dungeon.character_sprite_group.update(event, level.dungeon.walls_sprite_group)
            if event.type == pygame.KEYUP:
                level.dungeon.character_sprite_group.update(event, level.dungeon.walls_sprite_group)

        with open(os.path.join('data', 'player_data.csv'), encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                health = row['health']
                hearing = row['hearing']
                speed = row['speed']

        level.dungeon.character_sprite_group.update(None, level.dungeon.walls_sprite_group)
        level.dungeon.ghost_sprite_group.update(None, level.dungeon.walls_sprite_group)
        for sprite in level.dungeon.all_sprites:
            level.camera.apply(sprite)
        level.camera.update(level.character, width, height)

        screen.fill((0, 0, 0))
        level.dungeon.all_sprites.draw(screen)

        font_size = 30
        font = pygame.font.SysFont('bahnschrift', font_size)
        text = font.render(health, True, (255, 255, 255))
        screen.blit(text, (75, 10))
        screen.blit(health_icon, (10, 10))

        text = font.render(hearing, True, (255, 255, 255))
        screen.blit(text, (75, 50))
        screen.blit(hearing_icon, (15, 50))

        text = font.render(speed, True, (255, 255, 255))
        screen.blit(text, (75, 90))
        screen.blit(speed_icon, (15, 90))

        level.inventory.draw(screen)

        pygame.display.flip() # todo wall class

        clock.tick(fps)
