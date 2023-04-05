from pynput.keyboard import Key


class Page:
    def __init__(self):
        self.contents = list()
        self._showed = False

    def get_contents(self):
        if self._showed:
            return tuple()
        self._showed = True
        return tuple(self.contents)

    def get_next_state(self, key):
        if key == Key.backspace:
            return 'prev'
        return ''

    def exit(self):
        self._showed = False
