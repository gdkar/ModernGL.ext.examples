from PyQt5 import QtOpenGL, QtWidgets, QtCore


VERSION = QtCore.PYQT_VERSION_STR


class QGLControllerWidget(QtOpenGL.QGLWidget):
    def __init__(self, app):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)
        super(QGLControllerWidget, self).__init__(fmt, None)
        self.timer = QtCore.QElapsedTimer()
        self.app = app

    def initializeGL(self):
        self.timer.restart()
        self.start_ticks = self.timer.elapsed()
        self.app = self.app()
        self.app.init()

    def paintGL(self):
        viewport = (0, 0, self.width(), self.height())

        now = self.timer.elapsed()
        time_delta = (now - self.start_ticks) / 1000
        self.start_ticks = now

        self.app.render(viewport, time_delta)
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
