from view.object_sprites import Wall1, Wall2, Wall3, Floor1, Floor2, Floor3


class LevelData:
    def __init__(self, dungeon_size, chest_count, wall_sprite, floor_sprite):
        self.dungeon_size = dungeon_size
        self.chest_count = chest_count
        self.wall_sprite = wall_sprite
        self.floor_sprite = floor_sprite


class LevelGetter:
    __LEVELS = [
        LevelData(4, 1, Wall1, Floor1),
        LevelData(6, 1, Wall1, Floor1),
        LevelData(8, 1, Wall1, Floor1),
        LevelData(10, 2, Wall2, Floor2),
        LevelData(10, 2, Wall2, Floor2),
        LevelData(10, 2, Wall2, Floor2),
        LevelData(15, 2, Wall3, Floor3),
        LevelData(15, 2, Wall3, Floor3),
        LevelData(15, 2, Wall3, Floor3),
        LevelData(19, 2, Wall3, Floor3),
    ]

    @staticmethod
    def get_level_by_num(num):
        return LevelGetter.__LEVELS[num - 1]
