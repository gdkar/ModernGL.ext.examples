import GLWindow


VERSION = GLWindow.__version__


class WindowData:
    def __init__(self, wnd):
        self._wnd = wnd

    def key_pressed(self, key):
        return self._wnd.key_pressed(key)

    def key_released(self, key):
        return self._wnd.key_released(key)

    def key_down(self, key):
        return self._wnd.key_down(key)

    def key_up(self, key):
        return self._wnd.key_up(key)

    @property
    def viewport(self):
        return self._wnd.viewport

    @property
    def size(self):
        return self._wnd.size

    @property
    def frame_time(self):
        return self._wnd.time_delta

    @property
    def mouse(self):
        return self._wnd.mouse


class Window:
    def __init__(self, app, size, title):
        self.title = title
        self.size = size
        self.app = app
        self.wnd = None
        self.wnd_data = None

    def prepare_wnd_data(self):
        pass

    def main_loop(self):
        self.wnd = GLWindow.create_window(self.size, title=self.title)
        self.wnd_data = WindowData(self.wnd)

        self.app = self.app()
        self.prepare_wnd_data()
        self.app.init(self.wnd_data)

        while self.wnd.update():
            self.prepare_wnd_data()
            self.app.render(self.wnd_data)
