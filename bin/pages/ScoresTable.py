from bin.pages.Page import Page
from pynput.keyboard import Key
from bin.Screen import Screen


class ScoresTable(Page):
    def __init__(self):
        super().__init__()
        self._screen = Screen()
        self._win_size = self._screen.get_win_size()
        self.contents.append('')
        self.contents.append('Press [Backspace] to go back')
        self._window = 1
        self._n_windows = 1
        self._table_data = list()

    def action(self, key, maze):
        super().action(key, maze)
        if key == Key.up:
            self._showed = False
            self._window = self._window - 1 if self._window > 1 else self._window
        if key == Key.down:
            self._showed = False
            self._window = self._window + 1 if self._window < self._n_windows else self._window

    def get_contents(self, maze):
        (win_w, win_h) = self._screen.get_win_size()
        if self._showed and win_w == self._win_size[0] and win_h == self._win_size[1]:
            return tuple()
        self._win_size = (win_w, win_h)
        table_size = win_h - 9
        table_size = 1 if table_size < 1 else table_size
        import os
        # noinspection PyBroadException
        try:
            os.chdir('saves')
            os.chdir('..')
        except:
            os.mkdir('saves')
        # noinspection PyBroadException
        try:
            f = open('saves/scores_table.csv', 'r')
            f.close()
        except:
            f = open('saves/scores_table.csv', 'w')
            f.close()
        with open('saves/scores_table.csv', 'r') as f:
            scores = f.read()
        self._table_data = list()
        for i in scores.split('\n'):
            self._table_data.append(i.split(','))
        self._table_data = self._table_data[:-1]
        self._n_windows = len(self._table_data) // table_size
        self._n_windows = self._n_windows + 1 if len(self._table_data) % table_size > 0 else self._n_windows
        self._window = self._n_windows if self._window > self._n_windows else self._window
        table = ' ____________________________________________________\n' \
                '|_Player_|_Maze_size_|_Timer_|_Date_______|_Time_____|\n' \
                '|        |           |       |            |          |\n'
        for i in range(table_size * (self._window - 1), min(table_size * self._window, len(self._table_data))):
            table += '|  ' + self._table_data[i][0] + ' ' * (6 - len(self._table_data[i][0])) + \
                     '|  ' + self._table_data[i][1] + ' ' * (9 - len(self._table_data[i][1])) + \
                     '| ' + self._table_data[i][2] + ' ' * (6 - len(self._table_data[i][2])) + \
                     '| ' + self._table_data[i][3] + ' ' * (11 - len(self._table_data[i][3])) + \
                     '| ' + self._table_data[i][4] + ' ' * (9 - len(self._table_data[i][4])) + \
                     '|\n'
        table += '|________|___________|_______|____________|__________|'
        self.contents[0] = table
        self.contents[1] = 'Press [Backspace] to go back,\n'\
                           '[Up] and [Down] to scroll' + \
                           ' (' + str(self._window) + '/' + str(self._n_windows) + ')'
        self._showed = True
        return tuple(self.contents)

    def exit(self):
        super().exit()
        self._window = 1
        self._n_windows = 1
        self._table_data = list()
