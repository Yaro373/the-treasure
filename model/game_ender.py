import view.lose
import view.win


def end_game(reason):
    if reason == 0:
        view.lose.lose_screen()
    elif reason == 1:
        view.win.win.win_screen()
