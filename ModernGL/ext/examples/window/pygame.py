import pygame
from pygame.locals import DOUBLEBUF, OPENGL


VERSION = pygame.__version__


class WindowData:
    def __init__(self):
        self.frame_time = None
        self.viewport = None
        self.size = None
        self.mouse = None

    def key_pressed(self, key):
        return False

    def key_released(self, key):
        return False

    def key_down(self, key):
        return False

    def key_up(self, key):
        return False


class Window:
    def __init__(self, app, size, title):
        self.title = title
        self.size = size
        self.app = app
        self.wnd = None
        self.wnd_data = None

    def prepare_wnd_data(self):
        width, height = self.size
        self.wnd_data.viewport = (0, 0, width, height)
        self.wnd_data.size = self.size
        self.wnd_data.mouse = (0, 0)

        now = pygame.time.get_ticks()
        self.wnd_data.frame_time = (now - self.start_ticks) / 1000
        self.start_ticks = now

    def main_loop(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        pygame.display.set_mode(self.size, DOUBLEBUF | OPENGL)

        self.start_ticks = pygame.time.get_ticks()
        self.wnd_data = WindowData()

        self.prepare_wnd_data()
        self.app = self.app(self.wnd_data)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.prepare_wnd_data()
            self.app.render()

            pygame.display.flip()
            pygame.time.wait(10)
