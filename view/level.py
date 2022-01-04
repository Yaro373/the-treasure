import pygame
import view.dungeon
import view.creature
import view.inventory
import parameters


class ChestInventoryNotInstalled(Exception):
    pass


class LevelCreator:
    @staticmethod
    def create_level(data):
        return Level(data['dungeon_size'])


class Level:
    def __init__(self, dungeon_size):
        self.dungeon_size = dungeon_size
        self.dungeon = view.dungeon.Dungeon(self.dungeon_size)
        self.camera = view.dungeon.Camera()
        self.character = view.creature.Character(parameters.CELL_SIZE, parameters.CELL_SIZE,
                                                 self.dungeon.character_sprite_group,
                                                 self.dungeon.all_sprites)
        self.inventories = [view.inventory.Inventory(5)]

    def set_chest_inventory(self, chest_inventory):
        self.inventories.append(chest_inventory)

    def close_chest_inventory(self):
        if len(self.inventories) < 2:
           raise ChestInventoryNotInstalled
        self.inventories.pop(-1)


class LevelManager:
    level_index = 0
    level = LevelCreator.create_level({'dungeon_size': 20})

    @staticmethod
    def get_current_level():
        return LevelManager.level