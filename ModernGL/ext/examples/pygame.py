import pygame
from pygame.locals import DOUBLEBUF, OPENGL


VERSION = pygame.__version__


class Window:
    def __init__(self, app, size, title):
        self.title = title
        self.size = size
        self.app = app
        self.wnd = None

    def main_loop(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        pygame.display.set_mode(self.size, DOUBLEBUF | OPENGL)
        self.app = self.app()
        self.app.init()

        viewport = (0, 0, self.size[0], self.size[1])
        start_ticks = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            now = pygame.time.get_ticks()
            time_delta = (now - start_ticks) / 1000
            start_ticks = now

            self.app.render(viewport, time_delta)

            pygame.display.flip()
            pygame.time.wait(10)
