from bin.pages.Page import Page
from pynput.keyboard import Key
import time


class HostWait(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Waiting for the guest.\n'
                             'Server started at:\n'
                             '')
        self.contents.append('Press [Backspace] to go back')
        self._time = time.time()
        self._server_started = False
        self._guest_on = False
        self._initialized = False

    def action(self, key, maze):
        super().action(key, maze)
        if time.time() - self._time > 0.05:
            self._time = time.time()
            if not self._server_started:
                with open('data/server_data', 'w') as f:
                    f.write('0')
                address = maze.server_start()
                self.contents[0] = 'Waiting for the guest.\nServer started at:\n' + address[0] + ':' + str(address[1])
                self._showed = False
                self._server_started = True
            if not self._initialized:
                self._initialized = maze.check_init()
            else:
                self._guest_on = maze.check_guest()
        if key == Key.backspace:
            maze.server_stop()

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        elif self._guest_on:
            return 'MazeTypeMenu'
        return ''

    def exit(self):
        super().exit()
        self._server_started = False
        self._guest_on = False
        self._initialized = False
