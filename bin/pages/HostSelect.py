from bin.pages.Page import Page
from bin.Screen import Screen
from pynput.keyboard import Key
import string


class HostSelect(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('')
        self.contents.append('')
        self._parts = ['Insert host server address and port:\n'
                       '_', '_._', '_._', '_._', '_:_', '_\n',
                       'Connection failed', '']
        self._field_1 = ''
        self._field_2 = ''
        self._field_3 = ''
        self._field_4 = ''
        self._field_port = ''
        self._field_active = 1
        self._screen = Screen()
        self._win_size = self._screen.get_win_size()
        self._prev_allowed = True
        self._conn_not_established = False

    def clear_fields(self):
        self._field_1 = ''
        self._field_2 = ''
        self._field_3 = ''
        self._field_4 = ''
        self._field_port = ''
        self._field_active = 1

    # noinspection DuplicatedCode
    def action(self, key, maze):
        super().action(key, maze)
        if type(key) != Key and key in string.digits and key != '':
            self._field_1 += (key if self._field_active == 1 else '')
            self._field_1 = '' if self._field_1 == '' else str(int(self._field_1))
            self._field_2 += (key if self._field_active == 2 else '')
            self._field_2 = '' if self._field_2 == '' else str(int(self._field_2))
            self._field_3 += (key if self._field_active == 3 else '')
            self._field_3 = '' if self._field_3 == '' else str(int(self._field_3))
            self._field_4 += (key if self._field_active == 4 else '')
            self._field_4 = '' if self._field_4 == '' else str(int(self._field_4))
            self._field_port += (key if self._field_active == 5 else '')
            self._field_port = '' if self._field_port == '' else str(int(self._field_port))
            self._conn_not_established = False
            self._showed = False
        elif self._field_active < 5 and (key == Key.right or key == Key.space or key == Key.enter):
            self._field_active += 1
            self._conn_not_established = False
            self._showed = False
        elif self._field_active > 1 and key == Key.left:
            self._field_active -= 1
            self._conn_not_established = False
            self._showed = False
        elif key == Key.backspace:
            if self._field_active == 1 and self._field_1 != '':
                self._field_1 = self._field_1[:-1]
                self._prev_allowed = False
                self._showed = False
            elif self._field_active == 2 and self._field_2 != '':
                self._field_2 = self._field_2[:-1]
                self._prev_allowed = False
                self._showed = False
            elif self._field_active == 3 and self._field_3 != '':
                self._field_3 = self._field_3[:-1]
                self._prev_allowed = False
                self._showed = False
            elif self._field_active == 4 and self._field_4 != '':
                self._field_4 = self._field_4[:-1]
                self._prev_allowed = False
                self._showed = False
            elif self._field_active == 5 and self._field_port != '':
                self._field_port = self._field_port[:-1]
                self._prev_allowed = False
                self._showed = False
            self._conn_not_established = False
        elif key == Key.enter and self._field_active == 5 and \
                self._field_1 != '' and \
                self._field_2 != '' and \
                self._field_3 != '' and \
                self._field_4 != '' and \
                self._field_port != '':
            self._conn_not_established = maze.connect_guest((self._field_1 + '.' + self._field_2 + '.' + self._field_3 +
                                                             '.' + self._field_4, int(self._field_port)))
            self._showed = False

    # noinspection DuplicatedCode
    def get_contents(self, maze):
        if self._showed:
            return tuple()
        self.contents[0] = self._parts[0]
        self.contents[0] += self._field_1 + ('|' if self._field_active == 1 else '') + self._parts[1] + self._field_2 + \
                            ('|' if self._field_active == 2 else '') + self._parts[2] + self._field_3 + \
                            ('|' if self._field_active == 3 else '') + self._parts[3] + self._field_4 + \
                            ('|' if self._field_active == 4 else '') + self._parts[4] + self._field_port + \
                            ('|' if self._field_active == 5 else '') + self._parts[5] + (self._parts[6] if
                                                                                         self._conn_not_established else
                                                                                         self._parts[7])
        self.contents[1] = 'Press [Backspace] to go back' if \
            self._field_1 == '' and self._field_2 == '' and self._field_3 == '' and self._field_4 == '' \
            and self._field_port == '' else 'Press [Backspace] to clear input'
        self._showed = True
        return tuple(self.contents)

    def get_next_state(self, key):
        if key == Key.backspace and self._field_1 == '' and self._field_2 == '' and \
                self._field_3 == '' and self._field_4 == '' and self._field_port == '' and \
                self._prev_allowed:
            return 'prev'
        self._prev_allowed = True
        if key == Key.enter and self._field_active == 5 and \
                self._field_1 != '' and \
                self._field_2 != '' and \
                self._field_3 != '' and \
                self._field_4 != '' and \
                self._field_port != '' and \
                not self._conn_not_established:
            return 'GuestWait'
        return ''
