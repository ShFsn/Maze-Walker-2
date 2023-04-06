from bin.Drawer import Screen
from bin.Maze import Maze
from bin.pages.TitleScreen import TitleScreen
from bin.pages.ModeMenu import ModeMenu
from bin.pages.MazeTypeMenu import MazeTypeMenu
from bin.pages.LoadMenu import LoadMenu
from bin.pages.WriteMenu import WriteMenu
from bin.pages.GamePage import GamePage

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
        self._screen = Screen()
        self._maze = Maze()
        self._title_screen = TitleScreen()
        self._mode_menu = ModeMenu()
        self._maze_type_menu = MazeTypeMenu()
        self._load_menu = LoadMenu()
        self._write_menu = WriteMenu()
        self._game_page = GamePage()

    def call(self, key):
        if self._state == 'TitleScreen':
            self._call_page(self._title_screen, key)
        elif self._state == 'ModeMenu':
            self._call_page(self._mode_menu, key)
        elif self._state == 'MazeTypeMenu':
            self._call_page(self._maze_type_menu, key)
        elif self._state == 'LoadMenu':
            self._call_page(self._load_menu, key)
        elif self._state == 'WriteMenu':
            self._call_page(self._write_menu, key)
        elif self._state == 'GamePage':
            self._call_page(self._game_page, key)

    def _call_page(self, page, key):
        self._screen.refresh(page.get_contents(self._maze))
        page.action(key, self._maze)
        if self._change_state(page.get_next_state(key)):
            page.exit()

    def _change_state(self, next_state):
        if next_state != '':
            if next_state == 'prev':
                next_state = self._state_prev.pop()
            elif next_state == 'restart':
                while next_state != 'ModeMenu':
                    next_state = self._state_prev.pop()
            else:
                self._state_prev.append(self._state)
            self._state = next_state
            return True
        return False
