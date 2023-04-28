from bin.pages.Page import Page
from pynput.keyboard import Key


class MazeTypeMenu(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Would You like to:\n'
                             '[1] Generate a new maze (DFS)\n'
                             '[2] Generate a new maze (MST)\n'
                             '[3] Load saved one')
        self.contents.append('Press [Backspace] to go back')

    def action(self, key, maze):
        super().action(key, maze)
        if key == Key.backspace and not maze.is_single() and maze.is_host():
            maze.server_disconnect()
            maze.server_stop()
        elif key == '1':
            maze.set_generator('DFS')
        elif key == '2':
            maze.set_generator('MST')

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res == 'prev':
            return 'restart'
        elif key == '1':
            return 'SizeSelect'
        elif key == '2':
            return 'SizeSelect'
        elif key == '3':
            return 'LoadMenu'
        return ''
