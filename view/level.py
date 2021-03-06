import view.dungeon
import view.creature
import view.inventory
import view.level_data
import model.data_saver
import model.value_manager
import parameters
import model.game_ender


main_inventory = 'main_inventory'
chest_inventory = 'chest_inventory'


class LevelCreator:
    @staticmethod
    def new_level(num):
        level_data = view.level_data.LevelGetter.get_level_by_num(num)
        data = view.dungeon.DungeonGenerator.generate(level_data.dungeon_size, level_data.ghosts_count)
        dungeon = view.dungeon.Dungeon(data[0], level_data.wall_sprite, level_data.floor_sprite,
                                       enemies_positions=data[1])
        items = model.value_manager.ValueManager.inventory
        x_pos = 1
        y_pos = 1
        return Level(dungeon, items,
                     x_pos * parameters.CELL_SIZE, y_pos * parameters.CELL_SIZE)

    @staticmethod
    def load_level(num):
        level_data = view.level_data.LevelGetter.get_level_by_num(num)
        data = model.data_saver.DataLoader.data
        dungeon = view.dungeon.Dungeon(data.level_map, level_data.wall_sprite, level_data.floor_sprite,
                                       chests_inventory=data.chests_data,
                                       enemies_positions=data.enemies_positions)
        x_pos, y_pos = data.hero_position
        return Level(dungeon, data.inventory,
                     x_pos * parameters.CELL_SIZE, y_pos * parameters.CELL_SIZE)


class Level:
    def __init__(self, dungeon, hero_items, x_pos, y_pos):
        self.dungeon_size = len(dungeon.data)
        self.dungeon = dungeon
        self.camera = view.dungeon.Camera()
        self.character = view.creature.Character(x_pos, y_pos, hero_items,
                                                 self.dungeon.character_sprite_group,
                                                 self.dungeon.all_sprites)
        self.main_inventory = view.inventory.Inventory(self.character.items)
        self.chest_inventory = None

    def open_chest_inventory(self, chest):
        self.chest_inventory = view.inventory.ChestInventory(chest)

    def close_chest_inventory(self):
        self.chest_inventory.check_temp()
        self.chest_inventory = None

    def draw_inventories(self):
        self.main_inventory.draw()
        if self.chest_inventory is not None:
            self.chest_inventory.draw()

    def reload_main_inventory(self):
        print(self.character.items)
        self.main_inventory = view.inventory.Inventory(self.character.items)

    def update_inventories(self, event):
        if self.main_inventory is not None:
            self.main_inventory.update(event)
        if self.chest_inventory is not None:
            self.chest_inventory.update(event)


class LevelManager:
    level_num = 0
    level = None

    @staticmethod
    def get_current_level():
        return LevelManager.level

    @staticmethod
    def next_level():
        if LevelManager.level_num == 10:
            model.game_ender.end_game(1)

        LevelManager.level_num += 1
        LevelManager.level.dungeon.kill()
        LevelManager.level = LevelCreator.new_level(LevelManager.level_num)

    @staticmethod
    def reload_level():
        LevelManager.level.dungeon.kill()
        LevelManager.level = LevelCreator.new_level(LevelManager.level_num)

    @staticmethod
    def load_level():
        LevelManager.level_num = model.data_saver.DataLoader.data.level_num
        if LevelManager.level_num == 0:
            LevelManager.level_num += 1
            LevelManager.level = LevelCreator.new_level(LevelManager.level_num)
        else:
            LevelManager.level = LevelCreator.load_level(LevelManager.level_num)
