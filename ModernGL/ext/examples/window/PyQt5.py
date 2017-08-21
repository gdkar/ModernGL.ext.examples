from PyQt5 import QtOpenGL, QtWidgets, QtCore
import time


class WindowData:
    def __init__(self):
        self.time = None
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


class QGLControllerWidget(QtOpenGL.QGLWidget):
    def __init__(self, app):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)

        super(QGLControllerWidget, self).__init__(fmt, None)

        self.wnd_data = WindowData()
        self.start_ticks = time.perf_counter()
        self.last_ticks = self.start_ticks
        self.app = app

    def prepare_wnd_data(self):
        width, height = self.width(), self.height()
        self.wnd_data.viewport = (0, 0, width, height)
        self.wnd_data.size = (width, height)
        self.wnd_data.mouse = (0, 0)

        now = time.perf_counter()
        self.wnd_data.time = now - self.start_ticks
        self.wnd_data.frame_time = now - self.last_ticks
        self.last_ticks = now

    def initializeGL(self):
        self.prepare_wnd_data()
        self.app = self.app(self.wnd_data)

    def paintGL(self):
        self.prepare_wnd_data()
        self.app.render()
        self.update()


def run_example(example, size, title):
    if title is None:
        title = '%s - %s - %s' % (example.__name__, 'ModernGL', 'PyQt5')

    qtapp = QtWidgets.QApplication([])
    wnd = QGLControllerWidget(example)
    wnd.setFixedSize(size[0], size[1])
    wnd.setWindowTitle(title)
    wnd.move(QtWidgets.QDesktopWidget().rect().center() - wnd.rect().center())
    wnd.show()
    qtapp.exec_()
