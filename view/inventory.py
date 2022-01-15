import pygame
import view.items
import view.level


class Temp:
    temp = None
    click_coord = None


class ReplaceItem:
    def __init__(self, start_from, start_cell_index, item_name, need_back):
        self.start_from = start_from
        self.start_cell_index = start_cell_index
        self.item_name = item_name
        self.need_back = need_back


class BaseInventory:
    def __init__(self, short_name, items, bg_color, c_color, h_c_color):
        self.short_name = short_name
        self.count = len(items)
        self.background_color = bg_color
        self.cell_color = c_color
        self.hovered_cell_color = h_c_color
        self.items = items

    def basic_draw(self, y_cf):
        screen = pygame.display.get_surface()

        w, h = screen.get_size()
        element_size = min((w // 4 * 3) // self.count, h // 10)  # Вычисленный/максимальный размер

        surface = pygame.Surface(
            (element_size * self.count - (element_size // 10 * (self.count - 1)),
             element_size))  # Размер всего инвентаря
        surface.fill(self.background_color)

        # Положение инвентаря
        x = (w - element_size * self.count) // 2 + (element_size // 10 * (self.count - 1)) // 2
        y = int(h * y_cf) - element_size

        mouse_pos = pygame.mouse.get_pos()
        n = 0
        for i in range(element_size // 10, surface.get_width(), element_size - element_size // 10):
            cell_x, cell_y = i, element_size // 10
            cell_size = element_size - element_size // 5

            if self.is_coord_in_cell(cell_x, cell_y, x, y, mouse_pos[0], mouse_pos[1], cell_size):
                pygame.draw.rect(surface, self.hovered_cell_color,
                                 (cell_x, cell_y, cell_size, cell_size))
            else:
                pygame.draw.rect(surface, self.cell_color, (cell_x, cell_y, cell_size, cell_size))

            if Temp.click_coord is not None \
                    and self.is_coord_in_cell(cell_x, cell_y, x, y,
                                              Temp.click_coord[0], Temp.click_coord[1], cell_size):
                Temp.click_coord = None
                if Temp.temp is None and self.items[n] in \
                        view.items.images.keys():
                    Temp.temp = ReplaceItem(self.short_name, n, self.items[n], True)
                    self.items[n] = None
                elif Temp.temp is not None:
                    p = self.items[n]
                    self.items[n] = Temp.temp.item_name
                    if Temp.temp.need_back and n == Temp.temp.start_cell_index and \
                            self.short_name == Temp.temp.start_from:
                        Temp.temp = None
                    elif Temp.temp.need_back:
                        Temp.temp = ReplaceItem(Temp.temp.start_from, Temp.temp.start_cell_index,
                                                p, False)
            if Temp.temp is not None and not Temp.temp.need_back and \
                    Temp.temp.start_cell_index == n and \
                    Temp.temp.start_from == self.short_name:
                self.items[n] = Temp.temp.item_name
                Temp.temp = None
            self.add_item_to_cell(self.items[n], surface, i, element_size)
            n += 1

        pygame.display.get_surface().blit(surface, (x, y))
        if Temp.temp is not None and Temp.temp.need_back:
            pygame.display.get_surface().blit(
                view.items.images[Temp.temp.item_name],
                (mouse_pos[0] - view.items.size // 2,
                 mouse_pos[1] - view.items.size // 2))


    @staticmethod
    def is_coord_in_cell(cell_x, cell_y, x, y, target_x, target_y, cell_size):
        return cell_x < (target_x - x) < (cell_x + cell_size) and \
               cell_y < (target_y - y) < (cell_y + cell_size)

    @staticmethod
    def add_item_to_cell(name, surface, i, element_size):
        if name is None:
            return
        image = view.items.images[name]
        image_part_size = image.get_rect().width // 2
        surface.blit(image, (i + (element_size - element_size // 5) // 2 - image_part_size,
                     element_size // 2 - image_part_size))

    @staticmethod
    def check_click():
        Temp.click_coord = pygame.mouse.get_pos()


class Inventory(BaseInventory):
    def __init__(self, items):
        # TODO чтение из файла
        super().__init__('main',
                         items,
                         (139, 69, 19),
                         (255, 222, 173),
                         (255, 255, 173))

    def set_count(self, count):
        self.count = count

    def draw(self):
        super().basic_draw(1)

    def check_use(self, event):
        if event.key == pygame.K_u:
            if Temp.temp is not None:
                view.items.Item.use(Temp.temp.item_name)
                Temp.temp = None


class ChestInventory(BaseInventory):
    def __init__(self, chest):
        super().__init__('chest',
                         chest.items,
                         (200, 200, 200),
                         (100, 100, 100),
                         (150, 150, 150))
        self.chest = chest

    def draw(self):
        super().basic_draw(0.5)
        self.chest.items = self.items.copy()