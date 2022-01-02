import pygame


class Inventory:
    def __init__(self, count):
        self.count = count
        self.background_color = (139, 69, 19)
        self.cell_color = (255, 222, 173)

    def set_count(self, count):
        self.count = count

    def draw(self, screen):
        w, h = screen.get_size()
        max_size = h // 10
        element_size = (w // 4 * 3) // self.count
        if element_size > max_size:
            element_size = max_size

        surface = pygame.Surface((element_size * self.count - (element_size // 10 * (self.count - 1)),
                                 element_size))
        x = (w - element_size * self.count) // 2 + (element_size // 10 * (self.count - 1)) // 2
        y = h - element_size
        surface.fill(self.background_color)
        for i in range(element_size // 10, surface.get_width(), element_size - element_size // 10):
            pygame.draw.rect(surface, self.cell_color, (i,
                                                        element_size // 10,
                                                        element_size - element_size // 5,
                                                        element_size - element_size // 5))
        screen.blit(surface, (x, y))
