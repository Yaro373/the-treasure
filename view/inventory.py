import pygame


class Inventory:
    def __init__(self, count):
        self.count = count
        self.background_color = (139, 69, 19)
        self.cell_color = (255, 222, 173)
        self.hovered_cell_color = (255, 255, 173)

    def set_count(self, count):
        self.count = count

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

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
            cell_x = i
            cell_y = element_size // 10
            cell_size = element_size - element_size // 5
            if cell_x < (mouse_pos[0] - x) < (cell_x + cell_size) and \
                    cell_y < (mouse_pos[1] - y) < (cell_y + cell_size):
                pygame.draw.rect(surface, self.hovered_cell_color, (cell_x, cell_y, cell_size, cell_size))
            else:
                pygame.draw.rect(surface, self.cell_color, (cell_x, cell_y, cell_size, cell_size))

        screen.blit(surface, (x, y))

