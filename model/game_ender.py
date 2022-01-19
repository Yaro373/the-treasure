import lose
import win


def end_game(reason):
    if reason == 0:
        lose.lose_screen()
    elif reason == 1:
        win.win_screen()
