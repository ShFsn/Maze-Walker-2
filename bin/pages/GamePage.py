from bin.pages.Page import Page
from pynput.keyboard import Key
import time
from datetime import datetime


class GamePage(Page):
    def __init__(self):
        super(GamePage, self).__init__()
        self._time_start = time.time()
        self._time_curr = time.time()
        self._timer_state = 0
        self._timer = 0
        self._timer_ai = time.time()
        self._ai_speed = 1
        self._move_keys = ['w', 'a', 's', 'd', Key.up, Key.left, Key.down, Key.right]
        self._moved = False
        self._conn_closed = False
        self._time = time.time()
        self._is_written = False
        self._is_finished = False

    def action(self, key, maze):
        super().action(key, maze)
        if time.time() - self._timer_ai > maze.get_AI_delay() and maze.is_with_ai() and not self._is_finished:
            self._showed = False
            self._timer_ai = time.time()
            maze.move_AI()
        if time.time() - self._time > 0.01:
            self._time = time.time()
            if maze.is_online() and maze.is_host():
                if self._moved:
                    maze.set_mp_pos(1, maze.get_pos(1))
                pos = maze.get_mp_pos(2)
                if pos != maze.get_pos(2) and pos != (-1, -1):
                    maze.set_pos(2, pos)
                    maze.hide_path()
                    self._showed = False
            elif maze.is_online() and not maze.is_host():
                if maze.check_disconnect():
                    self._conn_closed = True
                    return
                if self._moved:
                    maze.set_mp_pos(2, maze.get_pos(2))
                pos = maze.get_mp_pos(1)
                if pos != maze.get_pos(1) and pos != (-1, -1):
                    maze.set_pos(1, pos)
                    maze.hide_path()
                    self._showed = False
        if self._timer_state == 0:
            self._time_start = time.time()
            self._timer_state = 1
        if self._timer_state == 1:
            self._time_curr = time.time()
        timer = int(self._time_curr - self._time_start) + maze.get_timer()
        if timer != self._timer:
            self._timer = timer
            self._showed = False
        if maze.is_finished():
            self._is_finished = True
            self._timer_state = 2
            if not self._is_written:
                self._is_written = True
                # noinspection PyBroadException
                try:
                    f = open('saves/scores_table.csv', 'r')
                    f.close()
                except:
                    f = open('saves/scores_table.csv', 'w')
                    f.close()
                with open('saves/scores_table.csv', 'r') as f:
                    old_scores = f.read()
                scores = str(maze.is_finished()) + ','
                data = maze.get_data().split('\n')
                scores += data[0] + ' x ' + data[1] + ','
                minutes = str(int(self._timer // 60))
                while len(minutes) < 2:
                    minutes = '0' + minutes
                seconds = str(int(self._timer % 60))
                while len(seconds) < 2:
                    seconds = '0' + seconds
                scores += str(minutes + ':' + seconds) + ','
                dt = datetime.now()
                day = str(dt.day // 10) + str(dt.day % 10)
                month = str(dt.month // 10) + str(dt.month % 10)
                year = str(dt.year)
                hour = str(dt.hour // 10) + str(dt.hour % 10)
                minute = str(dt.minute // 10) + str(dt.minute % 10)
                second = str(dt.second // 10) + str(dt.second % 10)
                scores += str(day) + '-' + str(month) + '-' + str(year) + ','
                scores += str(hour) + ':' + str(minute) + ':' + str(second) + '\n'
                with open('saves/scores_table.csv', 'w') as f:
                    f.write(scores + old_scores)
        if key == '1' or (key == '2' and not maze.is_single()):
            maze.hide_path()
            maze.show_path(key)
            self._showed = False
        if key in self._move_keys:
            maze.hide_path()
            self._showed = False
        if key == Key.backspace:
            maze.hide_path()
            maze.set_timer(self._timer)
            if maze.is_online() and maze.is_host():
                maze.server_disconnect()
                maze.server_stop()
        if key in self._move_keys:
            sides = ['up', 'left', 'down', 'right']
            i = 0
            while key != self._move_keys[i]:
                i += 1
            maze.move(i // 4 + 1, sides[i % 4])
            self._moved = True
            self._showed = False

    def get_contents(self, maze):
        if self._showed:
            return tuple()
        self._showed = True
        self.contents = list()
        self.contents.append(maze.get_picture())
        minutes = str(int(self._timer // 60))
        while len(minutes) < 2:
            minutes = '0' + minutes
        seconds = str(int(self._timer % 60))
        while len(seconds) < 2:
            seconds = '0' + seconds
        self.contents.append('Timer: ' + minutes + ':' + seconds + '\n'
                             'Show solution for: [1]' + ('' if maze.is_single() else ' / [2]') + '\n\n'
                             '[Backspace] to save and go to menu')
        return tuple(self.contents)

    def get_next_state(self, key):
        if key == Key.backspace or self._conn_closed:
            return 'WriteMenu'
        return ''

    def exit(self):
        super().exit()
        self._timer_state = 0
        self._conn_closed = False
        self._is_written = False
        self._is_finished = False
