from bin.pages.Page import Page
from pynput.keyboard import Key
import time


class GuestWait(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Waiting for maze creation.')
        self.contents.append('Press [Backspace] to go back')
        self._time = time.time()
        self._loaded = False
        self._conn_closed = False

    def action(self, key, maze):
        super().action(key, maze)
        if time.time() - self._time > 0.01:
            self._time = time.time()
            if maze.check_disconnect():
                self._conn_closed = True
                return
            data = maze.get_mp_maze()
            if data != '':
                maze.set_data(data)
                self._loaded = True

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        if self._loaded:
            return 'GamePage'
        elif self._conn_closed:
            return 'restart'
        return ''

    def exit(self):
        super().exit()
        self._loaded = False
        self._conn_closed = False
