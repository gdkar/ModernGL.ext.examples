import ModernGL

from ModernGL.ext.examples import run_example


class Example:
    def init(self, wnd):
        pass

    def render(self, wnd):
        print(wnd.viewport, wnd.frame_time)


# import logging
# log = logging.getLogger('ModernGL.ext.examples')
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)

run_example(Example)
