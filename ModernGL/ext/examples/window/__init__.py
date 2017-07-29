'''
    ModernGL example window
'''

import logging
import platform
import importlib

try:
    import ModernGL

except ImportError:
    ModernGL = None

try:
    import PIL

except ImportError:
    PIL = None

try:
    import pyrr

except ImportError:
    pyrr = None

log = logging.getLogger('ModernGL.ext.examples')

PLATFORM = platform.system().lower()
DEFAULT_BACKEND = 'GLWindow' if PLATFORM == 'windows' else 'PyQt5'
DEFAULT_FALLBACKS = 'PyQt5 pygame'


class ExampleWindow:
    def __init__(self, example, size, title, backend, fallbacks):
        self.backend = None

        try:
            self.impl = importlib.import_module('.' + backend, package='ModernGL.ext.examples.window')
            self.backend = backend

        except ImportError:
            log.debug('failed using backend %s', backend)

            if fallbacks:
                for fallback in fallbacks.split():
                    log.debug('trying fallback %s', fallback)

                    try:
                        self.impl = importlib.import_module('.' + fallback, package='ModernGL.ext.examples.window')
                        self.backend = fallback
                        break

                    except ImportError:
                        log.debug('failed using backend %s', fallback)

        if not self.backend:
            message = 'failed to find a window implementation'
            raise Exception(message)

        log.debug('success using backend %s', self.backend)
        log.debug('%s version: %s', self.backend, self.impl.VERSION)
        log.debug('ModernGL version: %s', ModernGL.__version__ if ModernGL else 'unknown')
        log.debug('Pillow version: %s', PIL.__version__ if PIL else 'unknown')
        log.debug('Pyrr version: %s', pyrr.__version__ if pyrr else 'unknown')

        if title is None:
            title = '%s - %s - %s' % (example.__name__, 'ModernGL', self.backend)

        self.wnd = self.impl.Window(example, size, title)

    def main_loop(self):
        self.wnd.main_loop()


def run_example(example, *, size=None, title=None, backend=DEFAULT_BACKEND, fallbacks=DEFAULT_FALLBACKS):
    '''
        Run example.

        Args:
            example (class): A class with a render method.

        Keyword Args:
            size (tuple): The size of the window.
            title (str): The title of the window.
            backend (str): The backend.
            fallbacks (str): The fallback backends.
    '''

    log.debug('platform: %s', PLATFORM)
    log.debug('backend: %s', backend)
    log.debug('fallbacks: %s', fallbacks)

    if size is None:
        size = (1280, 720)

    window = ExampleWindow(example, size, title, backend, fallbacks)
    window.main_loop()
