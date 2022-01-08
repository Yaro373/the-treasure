import os
import csv

import pygame.time


class ValueManager:
    with open(os.path.join('data', 'player_data.csv'), encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            health = int(row['health'])
            hearing = int(row['hearing'])
            speed = int(row['speed'])
            light = int(row['light'])
    update_health_data = []
    update_hearing_data = []
    update_speed_data = []
    update_light_data = []

    @staticmethod
    def update_health(add, for_time=-1):
        health = ValueManager.health
        ValueManager.health = min(ValueManager.health + add, 100)
        ValueManager.update_health_data.append((ValueManager.health - health, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_hearing(add, for_time=-1):
        hearing = ValueManager.hearing
        ValueManager.hearing = min(ValueManager.hearing + add, 100)
        ValueManager.update_hearing_data.append((ValueManager.hearing - hearing, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_speed(add, for_time=-1):
        speed = ValueManager.speed
        ValueManager.speed = min(ValueManager.speed + add, 5)
        ValueManager.update_speed_data.append((ValueManager.speed - speed, for_time, pygame.time.get_ticks()))

    @staticmethod
    def update_light(add, for_time=-1):
        light = ValueManager.light
        ValueManager.light = min(ValueManager.light + add, 7)
        ValueManager.update_light_data.append((ValueManager.light - light, for_time, pygame.time.get_ticks()))
        print(ValueManager.light)

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
        ValueManager.health = min(ValueManager.health, 100)
        ValueManager.hearing = min(ValueManager.hearing, 12)
        ValueManager.speed = min(ValueManager.speed, 5)
