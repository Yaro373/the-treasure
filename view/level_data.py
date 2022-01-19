from view.object_sprites import Wall1, Wall2, Wall3, Floor1, Floor2, Floor3


class LevelData:
    def __init__(self, dungeon_size, chest_count, wall_sprite, floor_sprite, ghosts_count):
        self.dungeon_size = dungeon_size
        self.chest_count = chest_count
        self.wall_sprite = wall_sprite
        self.floor_sprite = floor_sprite
        self.ghosts_count = ghosts_count


class LevelGetter:
    __LEVELS = [
        LevelData(4, 1, Wall1, Floor1, [1, 0, 0]),
        LevelData(6, 1, Wall1, Floor1, [2, 0, 0]),
        LevelData(8, 1, Wall1, Floor1, [2, 1, 0]),
        LevelData(10, 2, Wall2, Floor2, [2, 2, 0]),
        LevelData(10, 2, Wall2, Floor2, [1, 1, 1]),
        LevelData(10, 2, Wall2, Floor2, [2, 1, 1]),
        LevelData(15, 2, Wall3, Floor3, [2, 2, 1]),
        LevelData(15, 2, Wall3, Floor3, [3, 2, 1]),
        LevelData(15, 2, Wall3, Floor3, [4, 2, 1]),
        LevelData(19, 2, Wall3, Floor3, [4, 3, 1]),
    ]

    @staticmethod
    def get_level_by_num(num):
        return LevelGetter.__LEVELS[num - 1]
