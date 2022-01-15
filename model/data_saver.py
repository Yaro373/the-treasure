import csv
import os
import model.value_manager
import view.level
import model.value_manager


class DataSaver:
    @staticmethod
    def save():
        DataSaver.__save_characteristics()
        DataSaver.__save_current_level_map()
        DataSaver.__save_enemies_positions()
        DataSaver.__save_hero_position()
        DataSaver.__save_chests_data()
        DataSaver.__save_inventory()

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
    def __save_inventory():
        items = model.value_manager.ValueManager.inventory
        save_items = ';'.join(map(str, items))
        with open(DataSaver.__make_path('items.txt'), 'wt', encoding='utf-8') as file:
            print(save_items, file=file)

    @staticmethod
    def __make_path(name):
        return os.path.join('data', name)


class DataLoader:
    data = None

    @staticmethod
    def load():
        characteristics = DataLoader.__load_characteristics()
        level_map = DataLoader.__load_current_level_map()
        enemies_positions = DataLoader.__load_enemies_positions()
        hero_position = DataLoader.__load_hero_position()
        chests_data = DataLoader.__load_chests_data()
        inventory = DataLoader.__load_inventory()
        DataLoader.data = Data(characteristics, level_map, enemies_positions, hero_position,
                               chests_data, inventory)
        print(characteristics)

    @staticmethod
    def __load_characteristics():
        data = model.value_manager.ValueManager.get_data_to_save()
        with open(DataLoader.__make_path('player_data.csv'), 'rt', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=data.keys())
            next(reader)
            row = next(reader)
            return {
                'health': row['health'],
                'hearing': row['hearing'],
                'speed': row['speed'],
                'light': row['light'],
            }

    @staticmethod
    def __load_current_level_map():
        with open(DataLoader.__make_path('level.txt'), 'rt', encoding='utf-8') as file:
            result = [list(line) for line in file.readlines()]
            for i in range(len(result)):
                result[i].remove('\n')
                result[i] = list(map(int, result[i]))
            return result


    @staticmethod
    def __load_enemies_positions():
        with open(DataLoader.__make_path('enemies.txt'), 'rt', encoding='utf-8') as file:
            return [tuple(map(int, line.split())) for line in file.readlines()]

    @staticmethod
    def __load_hero_position():
        with open(DataLoader.__make_path('hero_pos.txt'), 'rt', encoding='utf-8') as file:
            return list(map(int, file.readline().split()))

    @staticmethod
    def __load_chests_data():
        with open(DataLoader.__make_path('chests.csv'), 'rt', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = dict()
            for line in reader:
                coords = tuple(map(int, line['coord'].split(';')))
                inventory = list(map(str, line['inventory'].split(';')))
                for i in range(0, len(inventory)):
                    if inventory[i] == 'None':
                        inventory[i] = None
                data[(coords[0], coords[1])] = (bool(line['opened']),
                                                inventory)
            print(data)
            return data

    @staticmethod
    def __load_inventory():
        with open(DataLoader.__make_path('items.txt'), 'rt', encoding='utf-8') as file:
            result = file.readline().rstrip().split(';')
            for i in range(len(result)):
                if result[i] == 'None':
                    result[i] = None
            model.value_manager.ValueManager.set_inventory(result)
            return result

    @staticmethod
    def __make_path(name):
        return os.path.join('data', name)


class Data:
    def __init__(self, characteristics, level_map, enemies_positions, hero_position,
                 chests_data, inventory):
        self.characteristics = characteristics
        self.level_map = level_map
        self.enemies_positions = enemies_positions
        self.hero_position = hero_position
        self.chests_data = chests_data
        self.inventory = inventory
