from bin.pages.Page import Page
from bin.Screen import Screen
from pynput.keyboard import Key
import string


class SizeSelect(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('')
        self.contents.append('')
        self._parts = ['Select size of your maze (', ' x ', ' max recommended', 'window size is too small',
                       '):\n\nHeight: _', '_   Width: _', '_']
        self._field_h_recommended = ''
        self._field_w_recommended = ''
        self._field_h_inserted = ''
        self._field_w_inserted = ''
        self._field_active = 1
        self._screen = Screen()
        self._win_size = self._screen.get_win_size()
        self._prev_allowed = True

    def clear_fields(self):
        self._field_h_inserted = ''
        self._field_w_inserted = ''
        self._field_active = 1

    def action(self, key, maze):
        if type(key) != Key and key in string.digits and key != '':
            self._field_h_inserted += (key if self._field_active == 1 else '')
            self._field_h_inserted = '' if self._field_h_inserted == '' or self._field_h_inserted == '0' \
                else str(int(self._field_h_inserted))
            self._field_w_inserted += (key if self._field_active == 2 else '')
            self._field_w_inserted = '' if self._field_w_inserted == '' or self._field_h_inserted == '0' \
                else str(int(self._field_w_inserted))
            self._showed = False
        elif self._field_active == 1 and (key == Key.right or key == Key.space or key == Key.enter):
            self._field_active = 2
            self._showed = False
        # elif self._field_active == 2 and (key == Key.left or (key == Key.backspace and self._field_w_inserted == '')):
        elif self._field_active == 2 and key == Key.left:
            self._field_active = 1
            self._showed = False
        elif key == Key.backspace:
            if self._field_active == 1 and self._field_h_inserted != '':
                self._field_h_inserted = self._field_h_inserted[:-1]
                self._prev_allowed = False
                self._showed = False
            elif self._field_active == 2 and self._field_w_inserted != '':
                self._field_w_inserted = self._field_w_inserted[:-1]
                self._prev_allowed = False
                self._showed = False
        elif key == Key.enter and self._field_active == 2 and self._field_h_inserted != '' and \
                self._field_w_inserted != '':
            maze.set_size(int(self._field_h_inserted), int(self._field_w_inserted))

    def get_contents(self, maze):
        (win_w, win_h) = self._screen.get_win_size()
        if self._showed and win_w == self._win_size[0] and win_h == self._win_size[1]:
            return tuple()
        self._win_size = (win_w, win_h)
        win_h -= 8
        win_w -= 3
        self._field_h_recommended = str(((win_h // 3) + 1) // 2)
        self._field_w_recommended = str(((win_w // 6) + 1) // 2)
        self.contents[0] = self._parts[0]
        self.contents[0] += (self._field_h_recommended + self._parts[1] + self._field_w_recommended +
                             self._parts[2]) if int(self._field_h_recommended) > 1 and \
                                                int(self._field_w_recommended) > 1 else self._parts[3]
        self.contents[0] += self._parts[4] + self._field_h_inserted + ('|' if self._field_active == 1 else '') + \
                            self._parts[5] + self._field_w_inserted + ('|' if self._field_active == 2 else '') + \
                            self._parts[6]
        self.contents[1] = 'Press [Backspace] to go back' if \
            self._field_h_inserted == '' and self._field_w_inserted == '' else 'Press [Backspace] to clear input'
        self._showed = True
        return tuple(self.contents)

    def get_next_state(self, key):
        if key == Key.backspace and self._field_h_inserted == '' and self._field_w_inserted == '' and \
                self._prev_allowed:
            return 'prev'
        self._prev_allowed = True
        if key == Key.enter and self._field_active == 2 and self._field_h_inserted != '' and \
                self._field_w_inserted != '':
            return 'PointsPosSelect'
        return ''
