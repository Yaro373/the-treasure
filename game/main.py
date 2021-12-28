import pygame
import game.view.сharacter
from game.view.dungeon import Dungeon, Camera, cell_size
from parameters import GAME_TITLE


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_TITLE)
    loop = True
    dungeon = Dungeon(20)
    camera = Camera()
    character = game.view.сharacter.Character(cell_size, cell_size,
                                              dungeon.character_sprite_group, dungeon.all_sprites)

    fps = 60
    clock = pygame.time.Clock()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                dungeon.character_sprite_group.update(event, dungeon.walls_sprite_group)
            if event.type == pygame.KEYUP:
                dungeon.character_sprite_group.update(event, dungeon.walls_sprite_group)
        dungeon.character_sprite_group.update(None, dungeon.walls_sprite_group)
        for sprite in dungeon.all_sprites:
            camera.apply(sprite)

        camera.update(character, width, height)
        screen.fill((0, 0, 0))
        dungeon.walls_sprite_group.draw(screen)
        dungeon.floor_sprite_group.draw(screen)
        dungeon.character_sprite_group.draw(screen)

        clock.tick(fps)
        pygame.display.flip() # todo wall class
