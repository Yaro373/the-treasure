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
        DataSaver.__save_level_num()
        DataSaver.__save_update_data()

    @staticmethod
    def __save_characteristics():
        data = model.value_manager.ValueManager.get_data_to_save()
        with open(DataSaver.__make_path('player_data.csv'), 'wt', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    @staticmethod
    def __save_current_level_map():
        if view.level.LevelManager.get_current_level() is None:
            return
        data = view.level.LevelManager.get_current_level().dungeon.data
        with open(DataSaver.__make_path('level.txt'), 'wt', encoding='utf-8') as file:
            for line in data:
                print(''.join(map(str, line)), file=file)

    @staticmethod
    def __save_enemies_positions():
        if view.level.LevelManager.get_current_level() is None:
            return
        ghosts = view.level.LevelManager.get_current_level().dungeon.ghost_sprite_group
        with open(DataSaver.__make_path('enemies.txt'), 'wt', encoding='utf-8') as file:
            for ghost in ghosts:
                print(' '.join(map(str, ghost.get_dung_coords())), file=file, end=' ')
                print(ghost.get_level(), file=file)

    @staticmethod
    def __save_hero_position():
        if view.level.LevelManager.get_current_level() is None:
            return
        coords = view.level.LevelManager.get_current_level().character.get_dung_coords()
        with open(DataSaver.__make_path('hero_pos.txt'), 'wt', encoding='utf-8') as file:
            print(' '.join(map(str, coords)), file=file)

    @staticmethod
    def __save_chests_data():
        if view.level.LevelManager.get_current_level() is None:
            return
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
    def __save_level_num():
        with open(DataSaver.__make_path('level_num.txt'), 'wt', encoding='utf-8') as file:
            print(view.level.LevelManager.level_num, file=file)

    @staticmethod
    def __save_update_data():
        with open(DataSaver.__make_path('update_data.txt'), 'wt', encoding='utf-8') as file:
            data = model.value_manager.ValueManager.get_string_to_save()
            for element in data:
                for el in element:
                    print(el, file=file)
                print(file=file)

    @staticmethod
    def __make_path(name):
        return os.path.join('data', name)


class DefaultDataSaver:
    @staticmethod
    def save():
        DefaultDataSaver.__save_characteristics()
        DefaultDataSaver.__save_current_level_map()
        DefaultDataSaver.__save_enemies_positions()
        DefaultDataSaver.__save_hero_position()
        DefaultDataSaver.__save_chests_data()
        DefaultDataSaver.__save_inventory()
        DefaultDataSaver.__save_level_num()
        DefaultDataSaver.__save_update_data()

    @staticmethod
    def __save_characteristics():
        data = {
            'health': 100,
            'hearing': 7,
            'speed': 1,
            'light': 5,
        }
        with open(DefaultDataSaver.__make_path('player_data.csv'), 'wt', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    @staticmethod
    def __save_current_level_map():
        with open(DefaultDataSaver.__make_path('level.txt'), 'wt', encoding='utf-8') as file:
            print('', file=file)

    @staticmethod
    def __save_enemies_positions():
        with open(DefaultDataSaver.__make_path('enemies.txt'), 'wt', encoding='utf-8') as file:
            print('', file=file)

    @staticmethod
    def __save_hero_position():
        with open(DefaultDataSaver.__make_path('hero_pos.txt'), 'wt', encoding='utf-8') as file:
            print('1 1', file=file)

    @staticmethod
    def __save_chests_data():
        with open(DefaultDataSaver.__make_path('chests.csv'), 'wt', newline='') as csvfile:
            print('', file=csvfile)

    @staticmethod
    def __save_inventory():
        items = ['oil', None, None, None, None]
        save_items = ';'.join(map(str, items))
        with open(DefaultDataSaver.__make_path('items.txt'), 'wt', encoding='utf-8') as file:
            print(save_items, file=file)

    @staticmethod
    def __save_level_num():
        with open(DefaultDataSaver.__make_path('level_num.txt'), 'wt', encoding='utf-8') as file:
            print('0', file=file)

    @staticmethod
    def __save_update_data():
        with open(DefaultDataSaver.__make_path('update_data.txt'), 'wt', encoding='utf-8') as file:
            print('empty\n\nempty\n\nempty\n\nempty\n\nNone\n\nNone', file=file)

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
        level_num = DataLoader.__load_level_num()
        update_data = DataLoader.__load_update_data()
        DataLoader.data = Data(characteristics, level_map, level_num, enemies_positions, hero_position,
                               chests_data, inventory, update_data)

    @staticmethod
    def __load_characteristics():
        try:
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
        except FileNotFoundError:
            DefaultDataSaver.save()

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
            data = [tuple(map(int, line.split())) for line in file.readlines()]
        result = [[], [], []]
        for el in data:
            result[el[2] - 1].append((el[0], el[1]))
        return result

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
    def __load_level_num():
        with open(DataLoader.__make_path('level_num.txt'), 'rt', encoding='utf-8') as file:
            result = int(file.readline().rstrip())
            return result

    @staticmethod
    def __load_update_data():
        with open(DataLoader.__make_path('update_data.txt'), 'rt', encoding='utf-8') as file:
            lines = file.readlines()
            results = [[]]
            for line in lines:
                line = line.rstrip()
                if line == '':
                    results.append([])
                else:
                    results[-1].append(line)

            for i in range(len(results)):
                for j in range(len(results[i])):
                    if results[i][j] == 'empty':
                        results[i] = []
                        break
                    if results[i][j] == 'None':
                        results[i] = None
                        break
                    results[i][j] = results[i][j].split(',')
                    results[i][j] = list(map(int, results[i][j]))
                    results[i][j] = tuple(results[i][j])

            return UpdateCharacteristicsData(results[0], results[1], results[2],
                                             results[3], results[4], results[5])

    @staticmethod
    def __make_path(name):
        return os.path.join('data', name)


class Data:
    def __init__(self, characteristics, level_map, level_num, enemies_positions, hero_position,
                 chests_data, inventory, update_data):
        self.characteristics = characteristics
        self.level_map = level_map
        self.level_num = level_num
        self.enemies_positions = enemies_positions
        self.hero_position = hero_position
        self.chests_data = chests_data
        self.inventory = inventory
        self.update_data = update_data


class UpdateCharacteristicsData:
    def __init__(self, update_health_data, update_hearing_data,
                 update_speed_data, update_light_data, update_inventory_data,
                 visibility_data):
        self.update_health_data = update_health_data
        self.update_hearing_data = update_hearing_data
        self.update_speed_data = update_speed_data
        self.update_light_data = update_light_data
        self.update_inventory_data = update_inventory_data
        self.visibility_data = visibility_data
