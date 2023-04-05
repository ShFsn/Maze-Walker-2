import bin.Drawer as Drawer
import bin.pages.TitleScreen as TitleScreen
import bin.pages.StartMenu as StartMenu

"""if key == '':
    ...
elif type(key) == Key:
    if key == Key.enter:
        self._input = ''
else:
    self._input += key"""


class Sequencer:
    def __init__(self):
        self._state_prev = list()
        self._state = 'TitleScreen'
        self._screen = Drawer.Screen()
        self._title_screen = TitleScreen.TitleScreen()
        self._start_menu = StartMenu.StartMenu()

    def call(self, key):
        if self._state == 'TitleScreen':
            self._call_title_screen(key)
        elif self._state == 'StartMenu':
            self._call_start_menu(key)

    def _change_state(self, next_state):
        if next_state != '':
            if next_state == 'prev':
                next_state = self._state_prev.pop()
            else:
                self._state_prev.append(self._state)
            self._state = next_state
            return True
        return False

    def _call_title_screen(self, key):
        self._screen.refresh(self._title_screen.get_contents())
        if self._change_state(self._title_screen.get_next_state(key)):
            self._title_screen.exit()

    def _call_start_menu(self, key):
        self._screen.refresh(self._start_menu.get_contents())
        if self._change_state(self._start_menu.get_next_state(key)):
            self._start_menu.exit()
