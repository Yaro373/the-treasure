import pygame
import os.path
import view.level
import model.value_manager
import model.data_saver
import model.tip
from parameters import GAME_TITLE


if __name__ == '__main__':
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_TITLE)

    model.data_saver.DataLoader.load()

    # TODO смена уровней
    level_manager = view.level.LevelManager()
    level_manager.next_level()

    model.value_manager.ValueManager.initialize()
    level = level_manager.get_current_level()

    health_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_health.png')).convert_alpha()
    hearing_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_hearing.png')).convert_alpha()
    speed_icon = pygame.image.load(os.path.join('resources', 'sprites', '32x32_speed.png')).convert_alpha()

    font_size = 30
    font = pygame.font.SysFont('bahnschrift', font_size)

    loop = True

    fps = 60
    clock = pygame.time.Clock()
    while loop:
        events = False
        for event in pygame.event.get():
            events = True
            if event.type == pygame.QUIT:
                model.data_saver.DataSaver.save()
                loop = False
            if event.type == pygame.KEYDOWN:
                level.dungeon.character_sprite_group.update(event)
                level.dungeon.chest_sprite_group.update(event)
                level.main_inventory.check_use(event)
            if event.type == pygame.KEYUP:
                level.dungeon.character_sprite_group.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level.chest_inventory is not None:
                    level.chest_inventory.check_click()
                level.main_inventory.check_click()
            level.dungeon.update(event)
        if not events:
            level.dungeon.update(None)

        level.dungeon.chest_sprite_group.update(None)
        level.dungeon.character_sprite_group.update(None)
        level.dungeon.ghost_sprite_group.update(None)
        level.dungeon.weapon_sprite_group.update()
        for sprite in level.dungeon.all_sprites:
            level.camera.apply(sprite)
        level.camera.update(level.character, *size)

        screen.fill((0, 0, 0))
        level.dungeon.all_sprites.draw(screen)

        text = font.render(model.value_manager.ValueManager.get_printable_health(), True, (255, 255, 255))
        screen.blit(text, (75, 10))
        screen.blit(health_icon, (10, 10))

        text = font.render(model.value_manager.ValueManager.get_printable_hearing(), True, (255, 255, 255))
        screen.blit(text, (75, 50))
        screen.blit(hearing_icon, (15, 50))

        text = font.render(model.value_manager.ValueManager.get_printable_speed(), True, (255, 255, 255))
        screen.blit(text, (75, 90))
        screen.blit(speed_icon, (15, 90))

        model.value_manager.ValueManager.update()
        model.tip.TipManager.show()

        level.draw_inventories()

        pygame.display.flip() # todo wall class

        clock.tick(fps)
