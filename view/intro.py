import pygame
import model.data_saver
import model.util


def show_intro(text_string):
    alpha = 0
    add = 1
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                model.util.terminate()

        w, h = screen.get_size()

        surface = pygame.surface.Surface((w, h))
        surface.fill((0, 0, 0))

        font = pygame.font.Font(None, 75)
        text = font.render(text_string, True, (255, 255, 255))
        text.set_alpha(alpha)
        text_x = w // 2 - text.get_width() // 2
        text_y = h // 2 - text.get_height() // 2
        surface.blit(text, (text_x, text_y))
        screen.blit(surface, (0, 0))

        alpha += add
        if alpha >= 100:
            add = -add
        elif alpha <= 0:
            loop = False

        pygame.display.flip()
        clock.tick(60)