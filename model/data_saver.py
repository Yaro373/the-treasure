import csv
import os
import model.value_manager
import view.level


class DataSaver:
    @staticmethod
    def save():
        DataSaver.__save_characteristics()
        DataSaver.__save_current_level_map()
        DataSaver.__save_enemies_positions()
        DataSaver.__save_hero_position()
        DataSaver.__save_chests_data()

    @staticmethod
    def __save_characteristics():
        data = model.value_manager.ValueManager.get_data_to_save()
        with open(DataSaver.__make_path('player_data.csv'), 'wt', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    @staticmethod
    def __save_current_level_map():
        data = view.level.LevelManager.get_current_level().dungeon.data
        with open(DataSaver.__make_path('level.txt'), 'wt', encoding='utf-8') as file:
            for line in data:
                print(''.join(map(str, line)), file=file)

    @staticmethod
    def __save_enemies_positions():
        ghosts = view.level.LevelManager.get_current_level().dungeon.ghost_sprite_group
        with open(DataSaver.__make_path('enemies.txt'), 'wt', encoding='utf-8') as file:
            for ghost in ghosts:
                print(' '.join(map(str, ghost.get_dung_coords())), file=file)

    @staticmethod
    def __save_hero_position():
        coords = view.level.LevelManager.get_current_level().character.get_dung_coords()
        with open(DataSaver.__make_path('hero_pos.txt'), 'wt', encoding='utf-8') as file:
            print(' '.join(map(str, coords)), file=file)

    @staticmethod
    def __save_chests_data():
        chest_sprite_group = view.level.LevelManager.get_current_level().dungeon.chest_sprite_group
        with open(DataSaver.__make_path('chests.csv'), 'wt', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['coord', 'opened', 'inventory'])
            writer.writeheader()
            for chest in chest_sprite_group:
                data = dict()
                data['coord'] = ';'.join(map(str, chest.get_dung_coords()))
                data['opened'] = chest.opened
                data['inventory'] = ';'.join(map(str, chest.items))
                writer.writerow(data)

    @staticmethod
    def __make_path(name):
        return os.path.join('data', name)