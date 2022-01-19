import pygame
import os.path
import view.level
import model.value_manager
import model.data_saver
import model.tip
import model.game_ender
import view.intro
from parameters import GAME_TITLE
from model.util import load_image, terminate


WIDTH = 800
HEIGHT = 600
FPS = 60


class Button(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("600x600_button_1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 0
        self.image2 = load_image("600x600_button_2.png")

    def change_sprite(self):
        self.image = self.image2


def start_screen():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))

    screen.blit(fon, (0, 0))
    sg = pygame.sprite.Group()
    button = Button(sg)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button.change_sprite()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    play()
                    return
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        sg.draw(screen)
        sg.update()
        pygame.display.flip()
        clock.tick(FPS)


def play():
    size = WIDTH, HEIGHT
    screen = pygame.display.get_surface()

    health_icon = pygame.image.load(
        os.path.join('resources', 'sprites', '32x32_health.png')).convert_alpha()
    hearing_icon = pygame.image.load(
        os.path.join('resources', 'sprites', '32x32_hearing.png')).convert_alpha()
    speed_icon = pygame.image.load(
        os.path.join('resources', 'sprites', '32x32_speed.png')).convert_alpha()

    font_size = 30
    font = pygame.font.SysFont('bahnschrift', font_size)

    loop = True

    fps = 60
    clock = pygame.time.Clock()

    while loop:
        events = False
        level = view.level.LevelManager.get_current_level()
        for event in pygame.event.get():
            events = True
            if event.type == pygame.QUIT:
                model.util.terminate()
                loop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                level.main_inventory.check_use(event)
            if event.type == pygame.KEYDOWN:
                level.dungeon.character_sprite_group.update(event)
                level.dungeon.chest_sprite_group.update(event)
            if event.type == pygame.KEYUP:
                level.dungeon.character_sprite_group.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                view.level.LevelManager.next_level()
                view.intro.show_intro(f'Уровень {view.level.LevelManager.level_num}')
            level.update_inventories(event)
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

        text = font.render(model.value_manager.ValueManager.get_printable_health(), True,
                           (255, 255, 255))
        screen.blit(text, (75, 10))
        screen.blit(health_icon, (10, 10))

        text = font.render(model.value_manager.ValueManager.get_printable_hearing(), True,
                           (255, 255, 255))
        screen.blit(text, (75, 50))
        screen.blit(hearing_icon, (15, 50))

        text = font.render(model.value_manager.ValueManager.get_printable_speed(), True,
                           (255, 255, 255))
        screen.blit(text, (75, 90))
        screen.blit(speed_icon, (15, 90))

        model.value_manager.ValueManager.update()
        model.tip.TipManager.show()

        level.draw_inventories()

        pygame.display.flip()  # todo wall class

        clock.tick(fps)


# управление wasd - перемещение V
# e - открыть сундук V
# z - следующий уровень V
# f - удалить предмет V
# space - выстрел V
# right mouse button - использовать предмет V


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GAME_TITLE)

    model.data_saver.DataLoader.load()

    view.level.LevelManager.load_level()
    model.value_manager.ValueManager.initialize()

    start_screen()
