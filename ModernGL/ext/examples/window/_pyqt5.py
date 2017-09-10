import time, sys, signal

import PyQt5.Qt as Q, PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets
from .interruptingcow import SignalWakeupHandler

class WindowData:
    def __init__(self):
        self.time = None
        self.frame_time = None
        self.viewport = None
        self.size = None
        self.ratio = None
        self.mouse = None

        self._key_state = [0] * 256

    def key_pressed(self, key):
        return self._key_state[key if type(key) is int else ord(key)] == 1

    def key_released(self, key):
        return self._key_state[key if type(key) is int else ord(key)] == 3

    def key_down(self, key):
        return self._key_state[key if type(key) is int else ord(key)] != 0

    def key_up(self, key):
        return self._key_state[key if type(key) is int else ord(key)] == 0


class QGLControllerWidget(Q.QOpenGLWidget):
    def __init__(self, app):
#        fmt = Q.()
#        fmt.setVersion(3, 3)
#        fmt.setProfile(fmt.CoreProfile)
        #fmt.setSampleBuffers(True)
#        fmt.setDepthBufferSize(24)

        super(QGLControllerWidget, self).__init__(None)
#        self.setFormat(fmt)
        self.setMouseTracking(True)

        self.wnd_data = WindowData()
        self.start_ticks = time.perf_counter()
        self.last_ticks = self.start_ticks
        self.key_down = [False] * 256
        self.mouse = (0, 0)
        self.app = app

    def prepare_wnd_data(self):
        width, height = self.width(), self.height()
        self.wnd_data.viewport = (0, 0, width, height)
        self.wnd_data.size = (width, height)
        self.wnd_data.ratio = width / height if height else 1.0
        self.wnd_data.mouse = self.mouse

        for i in range(256):
            if self.key_down[i]:
                if self.wnd_data._key_state[i] in (0, 1):
                    self.wnd_data._key_state[i] += 1

                elif self.wnd_data._key_state[i] == 3:
                    self.wnd_data._key_state[i] = 1

            else:
                if self.wnd_data._key_state[i] in (1, 2):
                    self.wnd_data._key_state[i] = 3

                elif self.wnd_data._key_state[i] == 3:
                    self.wnd_data._key_state[i] = 0

        now = time.perf_counter()
        self.wnd_data.time = now - self.start_ticks
        self.wnd_data.frame_time = now - self.last_ticks
        self.last_ticks = now

    def keyPressEvent(self, event):
        self.key_down[event.nativeVirtualKey() & 0xFF] = True

    def keyReleaseEvent(self, event):
        self.key_down[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event):
        self.mouse = (event.x(), self.height() - event.y() - 1)

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

    fmt = Q.QSurfaceFormat.defaultFormat()
    fmt.setVersion(4,5)
    fmt.setProfile(fmt.CoreProfile)
    fmt.setDepthBufferSize(24)
    Q.QSurfaceFormat.setDefaultFormat(fmt)
    Q.QCoreApplication.setAttribute(Q.Qt.AA_ShareOpenGLContexts)

    qtapp = Q.QApplication([])

    with SignalWakeupHandler(qtapp):
        signal.signal(signal.SIGINT,lambda *a:qtapp.quit())
        wnd = QGLControllerWidget(example)
        wnd.setWindowTitle(title)

        if size == 'fullscreen':
            wnd.showFullScreen()

        else:
            wnd.setFixedSize(size[0], size[1])
            wnd.move(Q.QDesktopWidget().rect().center() - wnd.rect().center())
            wnd.show()

        sys.exit(qtapp.exec_())
