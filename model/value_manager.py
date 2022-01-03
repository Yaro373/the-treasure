import os
import csv


class ValueManager:
    with open(os.path.join('data', 'player_data.csv'), encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            health = row['health']
            hearing = row['hearing']
            speed = row['speed']

    def set_health(self, health):
        ValueManager.health = health

    def set_hearing(self, hearing):
        ValueManager.hearing = hearing

    def set_speed(self, speed):
        ValueManager.speed = speed