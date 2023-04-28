from bin.pages.Page import Page
from pynput.keyboard import Key
import time


class GuestWait(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Waiting for maze creation.')
        self._time = time.time()
        self._loaded = False
        self._conn_closed = False

    def action(self, key, maze):
        super().action(key, maze)
        if time.time() - self._time > 0.05:
            self._time = time.time()
            data = maze.get_mp_maze()
            if data == 'closed':
                self._conn_closed = True
            elif data != '':
                maze.set_data(data)
                self._loaded = True
            print(data)

    def get_next_state(self, key):
        if self._loaded:
            return 'GamePage'
        elif self._conn_closed:
            return 'restart'
        return ''

    def exit(self):
        super().exit()
        self._loaded = False
        self._conn_closed = False
