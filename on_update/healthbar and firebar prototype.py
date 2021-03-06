import pygame
import os
import sys


HEALTH_COLOR = "#ff0d00"
DARK_HEALTH_COLOR = "#cc0a00"
FIRE_COLOR = "#ff6603"
DARK_FIRE_COLOR = "#ff1500"

high_heart_image_file_path = "64x64_heart_high.png"
mid_heart_image_file_path = "64x64_heart_mid.png"
low_heart_image_file_path = "64x64_heart_low.png"
high_fire_image_file_path = "64x64_fire_high.png"
mid_fire_image_file_path = "64x64_fire_mid.png"
low_fire_image_file_path = "64x64_fire_low.png"

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.abspath(os.path.join('resources', 'sprites', name))
    print(fullname)
    # если файл не существует, то выходим

    image = pygame.image.load(fullname)
    return image


class Bar:
    def __init__(self, x, y, param, max_value, min_value, image_high, image_mid,
                 mid_value, image_low, low_value):
        self.x = x
        self.y = y
        self.param = param
        self.high_image = image_high
        self.mid_image = image_mid
        self.low_image = image_low

        self.image_width = self.high_image.get_width()
        self.image_height = self.high_image.get_height()
        self.mid_value = mid_value
        self.low_value = low_value
        self.max_value = max_value
        self.min_value = min_value

        self.image = None
        self.change_image()

    def set_param(self, param):
        if param > self.max_value:
            self.param = self.max_value
        elif param < self.min_value:
            self.param = self.min_value
        else:
            self.param = param

    def get_param(self):
        return self.param

    def render(self, surface, x, y):
        surface.blit(self.image, (x, y))

    def change_image(self, rect_width=2, red_health_coef=0.82, color_dark=pygame.Color("black"),
                     color_light=pygame.Color("White")):
        x = self.x + self.image_width / 2
        y = self.y + self.image_height / 4
        w0 = self.image_width * 3
        w2 = w0 - rect_width * 2
        w4 = w0 - rect_width * 4
        h0 = self.image_height / 2
        h2 = h0 - rect_width * 2
        h4 = h0 - rect_width * 4
        surface = pygame.Surface((500, 500))
        print(self.image_width * self.x, self.image_width)

        # заполняем черным # 2
        pygame.draw.rect(surface, pygame.Color("black"),
                         (x,y,
                          w2,
                          h2), 0,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())

        # заполняем серым # 4
        pygame.draw.rect(surface, pygame.Color("grey"),
                         (x + rect_width * 2,
                          y + rect_width * 2,
                          w4,
                          (h4) * red_health_coef), 0,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())

        # заполняем темным цветом # 4
        pygame.draw.rect(surface, color_dark,
                         (x + rect_width * 2,
                          y + rect_width * 2,
                          w4 / self.max_value * self.param,
                          h4), 0,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())

        # заполняем светлым # 4
        pygame.draw.rect(surface, color_light,
                         (x + rect_width * 2,
                          y + rect_width * 2,
                          w4 / self.max_value * self.param,
                          h4 * red_health_coef), 0,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())
        # рисуем черную границу # 2
        pygame.draw.rect(surface, pygame.Color("black"),
                         (x + rect_width,
                          y + rect_width,
                          w2,
                          h2), rect_width,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())
        # рисуем белую границу # 0
        pygame.draw.rect(surface, pygame.Color("white"), (x,
                                                          y,
                                                          w0,
                                                          h0),
                         rect_width,
                         border_top_right_radius=self.high_image.get_height(),
                         border_bottom_right_radius=self.high_image.get_height())

        # рисуем
        if self.param > self.mid_value:
            surface.blit(self.high_image, (self.x,self.y))
        elif self.param > self.low_value:
            surface.blit(self.mid_image, (self.x,self.y))
        else:
            surface.blit(self.low_image, (self.x,self.y))
        self.image = surface
        print(surface)



class HealthBar(Bar):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 100, 0, load_image(high_heart_image_file_path),
                         load_image(mid_heart_image_file_path), 50,
                         load_image(low_heart_image_file_path), 25)

    def change_image(self):
        super().change_image(2, 0.82, pygame.Color(DARK_HEALTH_COLOR), pygame.Color(HEALTH_COLOR))

    def render(self, surface):
        super().render(surface, 0, 0)


class FireBar(Bar):
    def __init__(self, x, y):
        super().__init__(x, y, 7, 8, 0, load_image(high_fire_image_file_path),
                         load_image(mid_fire_image_file_path), 4,
                         load_image(low_fire_image_file_path), 1)

    def change_image(self):
        super().change_image(2, 0.82, pygame.Color(DARK_FIRE_COLOR), pygame.Color(FIRE_COLOR))

    def render(self, surface):
        super().render(surface, 0, 64)


# for work

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    loop = True

    healthbar = HealthBar(0,0)
    firebar = FireBar(0,-10)
    fps = 30
    clock = pygame.time.Clock()

    is_left_down = False
    is_right_down = False
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    is_left_down = True
                if event.key == pygame.K_RIGHT:
                    is_right_down = True
                if event.key == pygame.K_a:
                    firebar.set_param(firebar.get_param() - 1)
                    firebar.change_image()
                if event.key == pygame.K_d:
                    firebar.set_param(firebar.get_param() + 1)
                    firebar.change_image()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    is_left_down = False
                if event.key == pygame.K_RIGHT:
                    is_right_down = False
        if is_left_down:
            healthbar.set_param(healthbar.get_param() - 1 * clock.tick())
            healthbar.change_image()
        if is_right_down:
            healthbar.set_param(healthbar.get_param() + 1 * clock.tick())
            healthbar.change_image()
        # scene rendering
        screen.fill((0, 0, 0))
        healthbar.render(screen)
        firebar.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
