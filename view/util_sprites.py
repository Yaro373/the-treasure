import random

from model.util import load_image
import view.level
import pygame


class Arrow(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, *group):
        super().__init__(*group)
        self.direction = direction
        self.speed = 5
        self.level = view.level.LevelManager.get_current_level()

        if direction == 1:
            self.image = load_image('32x32_arrow1.png')
        elif direction == 2:
            self.image = load_image('32x32_arrow2.png')
        elif direction == 3:
            self.image = load_image('32x32_arrow3.png')
        else:
            self.image = load_image('32x32_arrow4.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        if self.direction in (2, 4):
            self.rect.y += random.randint(-4, 4)
        elif self.direction in (1, 3):
            self.rect.x += random.randint(-4, 4)

    def update(self):
        if self.direction == 1:
            self.rect.y -= self.speed
        elif self.direction == 2:
            self.rect.x += self.speed
        elif self.direction == 3:
            self.rect.y += self.speed
        elif self.direction == 4:
            self.rect.x -= self.speed

        if pygame.sprite.spritecollideany(self, self.level.dungeon.walls_sprite_group):
            self.kill()
        if ghost := pygame.sprite.spritecollideany(self, self.level.dungeon.ghost_sprite_group):
            self.kill()
            ghost.correct_health(-20)


class GhostBall(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, *group):
        super().__init__(*group)
        self.direction = direction
        self.speed = 5
        self.level = view.level.LevelManager.get_current_level()

        self.image = load_image('32x32_ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if self.direction in (2, 4):
            self.rect.y += random.randint(-4, 4)
        elif self.direction in (1, 3):
            self.rect.x += random.randint(-4, 4)

    def update(self):
        if self.direction == 1:
            self.rect.y -= self.speed
        elif self.direction == 2:
            self.rect.x += self.speed
        elif self.direction == 3:
            self.rect.y += self.speed
        elif self.direction == 4:
            self.rect.x -= self.speed

        if pygame.sprite.spritecollideany(self, self.level.dungeon.walls_sprite_group):
            self.kill()
        if character := pygame.sprite.spritecollideany(self, self.level.dungeon.character_sprite_group):
            self.kill()
            character.correct_health(-20)