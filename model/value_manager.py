import model.data_saver
import view.level
import pygame.time


class ValueManager:
    health = 100
    hearing = 7
    speed = 2
    light = 5
    inventory_size = 5

    inventory = [None, 'oil', 'oil', 'oil', None]
    update_health_data = []
    update_hearing_data = []
    update_speed_data = []
    update_light_data = []
    update_inventory_data = None
    visibility_data = None

    @staticmethod
    def initialize():
        if model.data_saver.DataLoader.data is not None:
            data = model.data_saver.DataLoader.data
            ValueManager.health = int(data.characteristics['health'])
            ValueManager.hearing = int(data.characteristics['hearing'])
            ValueManager.speed = int(data.characteristics['speed'])
            ValueManager.light = int(data.characteristics['light'])
            ValueManager.update_health_data = data.update_data.update_health_data
            ValueManager.update_hearing_data = data.update_data.update_hearing_data
            ValueManager.update_speed_data = data.update_data.update_speed_data
            ValueManager.update_light_data = data.update_data.update_light_data
            ValueManager.update_inventory_data = data.update_data.update_inventory_data
            ValueManager.visibility_data = data.update_data.visibility_data

    @staticmethod
    def set_invisibility(for_time):
        view.level.LevelManager.get_current_level().character.set_visibility(False)
        ValueManager.visibility_data = (for_time, pygame.time.get_ticks())

    @staticmethod
    def set_inventory_size(size, for_time=-1):
        ValueManager.inventory_size = size
        ValueManager.update_inventory_data = (size, for_time, pygame.time.get_ticks())

    @staticmethod
    def update_health(add, for_time=-1):
        health = ValueManager.health
        after = ValueManager.health + add
        ValueManager.health = min(after, 100)
        ValueManager.health = max(ValueManager.health, 0)
        ValueManager.update_health_data.append((ValueManager.health - health, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_hearing(add, for_time=-1):
        hearing = ValueManager.hearing
        after = ValueManager.hearing + add
        ValueManager.hearing = min(after, 100)
        ValueManager.hearing = max(ValueManager.hearing, 0)
        ValueManager.update_hearing_data.append((ValueManager.hearing - hearing, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_speed(add, for_time=-1):
        speed = ValueManager.speed
        after = ValueManager.speed + add
        ValueManager.speed = min(after, 5)
        ValueManager.speed = max(ValueManager.speed, 0)
        ValueManager.update_speed_data.append((ValueManager.speed - speed, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_light(add, for_time=-1):
        light = ValueManager.light
        after = ValueManager.light + add
        ValueManager.light = min(after, 7)
        ValueManager.light = max(ValueManager.light, 0)
        ValueManager.update_light_data.append((ValueManager.light - light, for_time, pygame.time.get_ticks()))

    @staticmethod
    def set_inventory(inventory):
        ValueManager.inventory = inventory

    @staticmethod
    def get_printable_health():
        return str(ValueManager.health)

    @staticmethod
    def get_printable_hearing():
        return str(ValueManager.hearing)

    @staticmethod
    def get_printable_speed():
        return str(ValueManager.speed)

    @staticmethod
    def get_data_to_save():
        return {
            'health': str(ValueManager.health),
            'hearing': str(ValueManager.hearing),
            'speed': str(ValueManager.speed),
            'light': str(ValueManager.light),
        }

    @staticmethod
    def is_visibility():
        return ValueManager.visibility_data is None

    @staticmethod
    def update():
        for el in ValueManager.update_health_data:
            if el[1] == -1:
                continue
            if pygame.time.get_ticks() - el[2] > el[1]:
                ValueManager.health += (-el[0])
                ValueManager.update_health_data.remove(el)
        for el in ValueManager.update_hearing_data:
            if el[1] == -1:
                continue
            if pygame.time.get_ticks() - el[2] > el[1]:
                ValueManager.hearing += (-el[0])
                ValueManager.update_hearing_data.remove(el)
        for el in ValueManager.update_speed_data:
            if el[1] == -1:
                continue
            if pygame.time.get_ticks() - el[2] > el[1]:
                ValueManager.speed += (-el[0])
                ValueManager.update_speed_data.remove(el)
        for el in ValueManager.update_light_data:
            if el[1] == -1:
                continue
            if pygame.time.get_ticks() - el[2] > el[1]:
                ValueManager.light += (-el[0])
                ValueManager.update_light_data.remove(el)
        if ValueManager.update_inventory_data is not None:
            if pygame.time.get_ticks() - ValueManager.update_inventory_data[2] > ValueManager.update_inventory_data[1]:
                ValueManager.update_inventory_data = None
                ValueManager.inventory_size = 5
        if ValueManager.visibility_data is not None:
            if pygame.time.get_ticks() - ValueManager.visibility_data[1] > \
                    ValueManager.visibility_data[0]:
                view.level.LevelManager.get_current_level().character.set_visibility(True)
                ValueManager.visibility_data = None
        ValueManager.health = min(ValueManager.health, 100)
        ValueManager.hearing = min(ValueManager.hearing, 12)
        ValueManager.speed = min(ValueManager.speed, 5)

    @staticmethod
    def get_string_to_save():
        time = pygame.time.get_ticks()

        health_ud = ValueManager._get_update_info_element_to_save(ValueManager.update_health_data)
        hearing_ud = ValueManager._get_update_info_element_to_save(ValueManager.update_hearing_data)
        speed_ud = ValueManager._get_update_info_element_to_save(ValueManager.update_speed_data)
        light_ud = ValueManager._get_update_info_element_to_save(ValueManager.update_light_data)

        el = ValueManager.update_inventory_data
        if el is not None:
            inventory_ud = ','.join(map(str, (el[0], el[1] - time + el[2], 0)))
        else:
            inventory_ud = ['None']

        el = ValueManager.visibility_data
        if el is not None:
            visibility_ud = ','.join(map(str, (el[0], el[1] - time + el[2], 0)))
        else:
            visibility_ud = ['None']

        return health_ud, hearing_ud, speed_ud, light_ud, inventory_ud, visibility_ud

    @staticmethod
    def _get_update_info_element_to_save(update_info_element):
        time = pygame.time.get_ticks()
        ud = update_info_element.copy()
        if ud:
            for i in range(len(ud)):
                el = ud[i]
                if el[1] < 0:
                    ud[i] = ''
                    continue
                ud[i] = ','.join(map(str, (el[0], el[1] - time + el[2], 0)))
        else:
            ud = ['empty']
        ud = list(filter(lambda x: x != '', ud))
        if len(ud) == 0:
            ud = ['empty']
        return ud