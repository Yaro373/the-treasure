import view.lose
import view.win
import model.data_saver
from main import start_screen


def end_game(reason):
    if reason == 0:
        view.lose.lose_screen()
    elif reason == 1:
        view.win.win_screen()


def start_new_game():
    model.data_saver.DefaultDataSaver.save()
    start_screen()

