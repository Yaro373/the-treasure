import pygame
import game.view.level
from parameters import GAME_TITLE


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_TITLE)
    level_manager = game.view.level.LevelManager()
    level = level_manager.get_current_level()
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
        level.dungeon.character_sprite_group.update(None, level.dungeon.walls_sprite_group)
        level.dungeon.ghost_sprite_group.update(None, level.dungeon.walls_sprite_group)
        for sprite in level.dungeon.all_sprites:
            level.camera.apply(sprite)

        level.camera.update(level.character, width, height)
        screen.fill((0, 0, 0))
        level.dungeon.walls_sprite_group.draw(screen)
        level.dungeon.floor_sprite_group.draw(screen)
        level.dungeon.character_sprite_group.draw(screen)
        level.dungeon.ghost_sprite_group.draw(screen)

        clock.tick(fps)
        pygame.display.flip() # todo wall class

