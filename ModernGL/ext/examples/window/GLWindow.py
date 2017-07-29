import GLWindow


VERSION = GLWindow.__version__


class Window:
    def __init__(self, app, size, title):
        self.title = title
        self.size = size
        self.app = app
        self.wnd = None

    def main_loop(self):
        self.wnd = GLWindow.create_window(self.size, title=self.title)
        self.app = self.app()
        self.app.init()

        while self.wnd.update():
            self.app.render(self.wnd.viewport, self.wnd.time_delta)
