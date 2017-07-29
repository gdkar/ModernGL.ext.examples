from PyQt5 import QtOpenGL, QtWidgets, QtCore


VERSION = QtCore.PYQT_VERSION_STR


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


class QGLControllerWidget(QtOpenGL.QGLWidget):
    def __init__(self, app):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)
        super(QGLControllerWidget, self).__init__(fmt, None)
        self.wnd_data = WindowData()
        self.timer = QtCore.QElapsedTimer()
        self.timer.restart()
        self.start_ticks = self.timer.elapsed()
        self.app = app

    def prepare_wnd_data(self):
        width, height = self.width(), self.height()
        self.wnd_data.viewport = (0, 0, width, height)
        self.wnd_data.size = (width, height)
        self.wnd_data.mouse = (0, 0)

        now = self.timer.elapsed()
        self.wnd_data.frame_time = (now - self.start_ticks) / 1000
        self.start_ticks = now

    def initializeGL(self):
        self.app = self.app()
        self.prepare_wnd_data()
        self.app.init(self.wnd_data)

    def paintGL(self):
        self.prepare_wnd_data()
        self.app.render(self.wnd_data)
        self.update()


class Window:
    def __init__(self, app, size, title):
        self.title = title
        self.size = size
        self.app = app
        self.wnd = None

    def main_loop(self):
        qtapp = QtWidgets.QApplication([])
        self.wnd = QGLControllerWidget(self.app)
        self.wnd.setFixedSize(self.size[0], self.size[1])
        self.wnd.setWindowTitle(self.title)
        self.wnd.move(QtWidgets.QDesktopWidget().rect().center() - self.wnd.rect().center())
        self.wnd.show()
        qtapp.exec_()
