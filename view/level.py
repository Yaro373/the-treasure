import pygame
import view.dungeon
import view.creature
import view.inventory
import parameters


main_inventory = 'main_inventory'
chest_inventory = 'chest_inventory'


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
        self.inventories = {main_inventory: view.inventory.Inventory(5),
                            chest_inventory: None}

    def open_chest_inventory(self, chest):
        self.inventories[chest_inventory] = view.inventory.ChestInventory(chest)

    def close_chest_inventory(self):
        self.inventories[chest_inventory] = None


class LevelManager:
    level_index = 0
    level = LevelCreator.create_level({'dungeon_size': 5})

    @staticmethod
    def get_current_level():
        return LevelManager.level
