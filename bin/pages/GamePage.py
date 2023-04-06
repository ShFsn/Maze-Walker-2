from bin.pages.Page import Page
from pynput.keyboard import Key
import time


class GamePage(Page):
    def __init__(self):
        super(GamePage, self).__init__()
        self._time_start = time.time()
        self._time_curr = time.time()
        self._timer_state = 0
        self._timer = 0
        self._move_keys = ['w', 'a', 's', 'd', Key.up, Key.left, Key.down, Key.right]

    def action(self, key, maze):
        if self._timer_state == 0:
            self._time_start = time.time()
            self._timer_state = 1
        if self._timer_state == 1:
            self._time_curr = time.time()
        if maze.is_finished():
            self._timer_state = 2
        timer = int(self._time_curr - self._time_start) + maze.get_timer()
        if timer != self._timer:
            self._timer = timer
            self._showed = False
        if key == '1' or (key == '2' and not maze.is_single()):
            maze.show_path(key)
            self._showed = False
        if key in self._move_keys:
            if maze.is_single() and key in self._move_keys[4:]:
                pass
            else:
                maze.hide_path()
                self._showed = False
        if key == Key.backspace:
            maze.hide_path()
            maze.set_timer(self._timer)
        ...

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
        if key == Key.backspace:
            return 'WriteMenu'
        return ''

    def exit(self):
        super().exit()
        self._timer_state = 0
