from game.model.util import load_image
import pygame


class Character(pygame.sprite.Sprite):
    image = load_image('32x32_character.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.f_x = 0
        self.f_y = 0
        self.speed = 4
        self.move_data = [0, 0, 0, 0]
        self.prev_collide = None

    def update(self, event, walls_sprite_group):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_data[0] = 1
                elif event.key == pygame.K_RIGHT:
                    self.move_data[1] = 1
                elif event.key == pygame.K_DOWN:
                    self.move_data[2] = 1
                elif event.key == pygame.K_LEFT:
                    self.move_data[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.move_data[0] = 0
                elif event.key == pygame.K_RIGHT:
                    self.move_data[1] = 0
                elif event.key == pygame.K_DOWN:
                    self.move_data[2] = 0
                elif event.key == pygame.K_LEFT:
                    self.move_data[3] = 0

        if self.move_data[0] == 1:
            self.rect.y -= self.speed
            self.f_y -= self.speed
        if pygame.sprite.spritecollideany(self, walls_sprite_group):
            self.rect.y += self.speed
            self.f_y += self.speed

        if self.move_data[1] == 1:
            self.rect.x += self.speed
            self.f_x += self.speed
        if pygame.sprite.spritecollideany(self, walls_sprite_group):
            self.rect.x -= self.speed
            self.f_x -= self.speed

        if self.move_data[2] == 1:
            self.rect.y += self.speed
            self.f_y += self.speed
        if pygame.sprite.spritecollideany(self, walls_sprite_group):
            self.rect.y -= self.speed
            self.f_y -= self.speed

        if self.move_data[3] == 1:
            self.rect.x -= self.speed
            self.f_x -= self.speed
        if pygame.sprite.spritecollideany(self, walls_sprite_group):
            self.rect.x += self.speed
            self.f_x += self.speed

