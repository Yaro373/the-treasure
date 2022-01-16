import model.data_saver
import view.level
import pygame.time


class ValueManager:
    health = None
    hearing = None
    speed = None
    light = None
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
            data = model.data_saver.DataLoader.data.characteristics
            ValueManager.health = int(data['health'])
            ValueManager.hearing = int(data['hearing'])
            ValueManager.speed = int(data['speed'])
            ValueManager.light = int(data['light'])

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
        ValueManager.health = max(after, 0)
        ValueManager.update_health_data.append((ValueManager.health - health, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_hearing(add, for_time=-1):
        hearing = ValueManager.hearing
        after = ValueManager.hearing + add
        ValueManager.hearing = min(after, 100)
        ValueManager.hearing = max(after, 0)
        ValueManager.update_hearing_data.append((ValueManager.hearing - hearing, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_speed(add, for_time=-1):
        speed = ValueManager.speed
        after = ValueManager.speed + add
        ValueManager.speed = min(after, 5)
        ValueManager.speed = max(after, 0)
        ValueManager.update_speed_data.append((ValueManager.speed - speed, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_light(add, for_time=-1):
        light = ValueManager.light
        after = ValueManager.light + add
        ValueManager.light = min(after, 7)
        ValueManager.light = max(after, 0)
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
