from bin.pages.Page import Page
from pynput.keyboard import Key
import string


class AISpeedSelect(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('')
        self.contents.append('')
        self._parts = ['Select AI move speed):\n\nMoves per 10 sec: _', '|_']
        self._field_speed = ''
        self._prev_allowed = True

    # noinspection DuplicatedCode
    def action(self, key, maze):
        super().action(key, maze)
        if type(key) != Key and key in string.digits and key != '':
            self._field_speed += key
            self._field_speed = '' if self._field_speed == '' or self._field_speed == '0' \
                else str(int(self._field_speed))
            self._showed = False
        elif key == Key.backspace and self._field_speed != '':
            self._field_speed = self._field_speed[:-1]
            self._prev_allowed = False
            self._showed = False
        elif key == Key.enter and self._field_speed != '':
            maze.set_AI_speed(int(self._field_speed) / 10)

    # noinspection DuplicatedCode
    def get_contents(self, maze):
        if self._showed:
            return tuple()
        self.contents[0] = self._parts[0] + self._field_speed + self._parts[1]
        self.contents[1] = 'Press [Backspace] to go back' if \
            self._field_speed == '' else 'Press [Backspace] to clear input'
        self._showed = True
        return tuple(self.contents)

    def get_next_state(self, key):
        if key == Key.backspace and self._field_speed == '' and self._prev_allowed:
            return 'prev'
        self._prev_allowed = True
        if key == Key.enter and self._field_speed != '':
            return 'MazeTypeMenu'
        return ''
