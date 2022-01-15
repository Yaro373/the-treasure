import pygame


class TipManager:
    tip = None
    start = -1
    duration = -1

    @staticmethod
    def create_tip(text, duration):
        TipManager.tip = Tip(text)
        TipManager.duration = duration
        TipManager.start = pygame.time.get_ticks()

    @staticmethod
    def show():
        if TipManager.tip is not None:
            if pygame.time.get_ticks() - TipManager.start < TipManager.duration:
                TipManager.tip.show()
            else:
                TipManager.stop_showing()

    @staticmethod
    def showing():
        return TipManager.tip

    @staticmethod
    def stop_showing():
        TipManager.tip = None


class Tip:
    def __init__(self, text):
        self.text = text
        self.start_time = -1

    def show(self):
        surface = pygame.display.get_surface()
        w, h = surface.get_size()
        font = pygame.font.Font(None, 25)
        text = font.render(self.text, True, (255, 255, 255))
        text_x = w // 2 - text.get_width() // 2
        text_y = h - 90
        surface.blit(text, (text_x, text_y))
