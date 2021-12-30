import pygame
import game.view.dungeon
import game.view.creature
import game.parameters


class LevelCreator:
    @staticmethod
    def create_level(data):
        return Level(data['dungeon_size'])


class Level:
    def __init__(self, dungeon_size):
        self.dungeon_size = dungeon_size
        self.dungeon = game.view.dungeon.Dungeon(self.dungeon_size)
        self.camera = game.view.dungeon.Camera()
        self.character = game.view.creature.Character(0, 0, self.dungeon.character_sprite_group,
                                                      self.dungeon.all_sprites)


class LevelManager:
    level_index = 0
    level = LevelCreator.create_level({'dungeon_size': 20})

    @staticmethod
    def get_current_level():
        return LevelManager.level