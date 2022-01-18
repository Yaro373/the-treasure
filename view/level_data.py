from view.object_sprites import Wall1, Wall2, Wall3, Floor1, Floor2, Floor3


class LevelData1:
    dungeon_size = 4
    chest_count = 1
    wall_sprite = Wall1
    floor_sprite = Floor1


class LevelData2:
    dungeon_size = 6
    chest_count = 1
    wall_sprite = Wall1
    floor_sprite = Floor1


class LevelData3:
    dungeon_size = 8
    chest_count = 1
    wall_sprite = Wall1
    floor_sprite = Floor1


class LevelData4:
    dungeon_size = 10
    chest_count = 2
    wall_sprite = Wall2
    floor_sprite = Floor2


class LevelData5:
    dungeon_size = 10
    chest_count = 2
    wall_sprite = Wall2
    floor_sprite = Floor2


class LevelData6:
    dungeon_size = 10
    chest_count = 2
    wall_sprite = Wall2
    floor_sprite = Floor2


class LevelData7:
    dungeon_size = 15
    chest_count = 2
    wall_sprite = Wall3
    floor_sprite = Floor3


class LevelData8:
    dungeon_size = 15
    chest_count = 2
    wall_sprite = Wall3
    floor_sprite = Floor3


class LevelData9:
    dungeon_size = 15
    chest_count = 2
    wall_sprite = Wall3
    floor_sprite = Floor3


class LevelData10:
    dungeon_size = 19
    chest_count = 2
    wall_sprite = Wall3
    floor_sprite = Floor3


class LevelGetter:
    __LEVELS = [
        LevelData1,
        LevelData2,
        LevelData3,
        LevelData4,
        LevelData5,
        LevelData6,
        LevelData7,
        LevelData8,
        LevelData9,
        LevelData10,
    ]

    def get_level_by_num(num):
        return LevelGetter.__LEVELS[num - 1]
