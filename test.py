import ModernGL

from ModernGL.ext.examples import run_example


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

    def render(self):
        print(self.wnd.viewport, self.wnd.frame_time)


# import logging
# log = logging.getLogger('ModernGL.ext.examples')
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)

run_example(Example)
