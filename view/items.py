from model.util import load_image

size = 48

RANDOM_ITEMS_LIST = {
    'tea': 0.25,
    'hot_tea': 0.15,
    'dream_catcher': 0.03,
    'bag': 0.15,
    'old_clock': 0.02,
    'hearing_potion': 0.10,
    'speed_potion': 0.10,
    'music_box': 0.05,
    'snow_ball': 0.05,
    'invisibility_potion': 0.10,
}

images = {
    'tea': load_image('48x48_tea.png'),
    'hot_tea': load_image('48x48_hot_tea.png'),
    'oil': load_image('48x48_oil.png'),
    'bag': load_image('48x48_bag.png'),
    'old_clock': load_image('48x48_old_clock.png'),
    'hearing_potion': load_image('48x48_hearing_potion.png'),
    'speed_potion': load_image('48x48_speed_potion.png'),
    'music_box': load_image('48x48_music_box.png'),
    'snow_ball': load_image('48x48_snow_ball.png'),
    'invisibility_potion': load_image('48x48_invisibility_potion.png'),
}