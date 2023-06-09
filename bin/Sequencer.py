from bin.Screen import Screen
from bin.Maze import Maze
from bin.pages.TitleScreen import TitleScreen
from bin.pages.ModeMenu import ModeMenu
from bin.pages.ScoresTable import ScoresTable
from bin.pages.AISpeedSelect import AISpeedSelect
from bin.pages.MazeTypeSelect import MazeTypeMenu
from bin.pages.SizeSelect import SizeSelect
from bin.pages.PointsPosSelect import PointsPosSelect
from bin.pages.LoadMenu import LoadMenu
from bin.pages.WriteMenu import WriteMenu
from bin.pages.GamePage import GamePage
from bin.pages.HostModeMenu import HostModeMenu
from bin.pages.HostWait import HostWait
from bin.pages.HostSelect import HostSelect
from bin.pages.GuestWait import GuestWait


class Sequencer:
    def __init__(self):
        self._state_prev = list()
        self._state = 'TitleScreen'
        self._screen = Screen()
        self._maze = Maze()
        self._title_screen = TitleScreen()
        self._mode_menu = ModeMenu()
        self._scores_table = ScoresTable()
        self._ai_speed_select = AISpeedSelect()
        self._maze_type_menu = MazeTypeMenu()
        self._size_select = SizeSelect()
        self._points_pos_select = PointsPosSelect()
        self._load_menu = LoadMenu()
        self._write_menu = WriteMenu()
        self._game_page = GamePage()
        self._host_mode_menu = HostModeMenu()
        self._host_wait = HostWait()
        self._host_select = HostSelect()
        self._guest_wait = GuestWait()

    def call(self, key):
        if self._state == 'TitleScreen':
            self._call_page(self._title_screen, key)
        elif self._state == 'ModeMenu':
            self._call_page(self._mode_menu, key)
        elif self._state == 'ScoresTable':
            self._call_page(self._scores_table, key)
        elif self._state == 'AISpeedSelect':
            self._call_page(self._ai_speed_select, key)
        elif self._state == 'MazeTypeMenu':
            self._call_page(self._maze_type_menu, key)
        elif self._state == 'SizeSelect':
            self._call_page(self._size_select, key)
        elif self._state == 'PointsPosSelect':
            self._call_page(self._points_pos_select, key)
        elif self._state == 'LoadMenu':
            self._call_page(self._load_menu, key)
        elif self._state == 'WriteMenu':
            self._call_page(self._write_menu, key)
        elif self._state == 'GamePage':
            self._call_page(self._game_page, key)
        elif self._state == 'HostModeMenu':
            self._call_page(self._host_mode_menu, key)
        elif self._state == 'HostWait':
            self._call_page(self._host_wait, key)
        elif self._state == 'HostSelect':
            self._call_page(self._host_select, key)
        elif self._state == 'GuestWait':
            self._call_page(self._guest_wait, key)

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
            if next_state == 'GamePage':
                self._size_select.clear_fields()
            return True
        return False
