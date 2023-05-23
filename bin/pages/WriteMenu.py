from bin.pages.SavesMenu import SavesMenu
from pynput.keyboard import Key


class WriteMenu(SavesMenu):
    def __init__(self):
        super().__init__()
        self.contents.append('[Backspace] to go to menu without saving')

    def get_contents(self, maze):
        if self._showed:
            return tuple()
        super().get_contents(maze)
        for i in range(5):
            self.contents[0] += '[' + str(i + 1) + '] Save ' + str(i + 1) + '\n'
        self._showed = True
        return tuple(self.contents)

    def action(self, key, maze):
        super().action(key, maze)
        save_num = self._assert_valid(key, list())
        if save_num < 0:
            return
        path = 'saves/' + ('single/' if maze.is_single() else 'multi/') + 'save_'
        data = maze.get_data()
        with open(path + key, 'w') as f:
            f.write(data)

    def get_next_state(self, key):
        save_num = self._assert_valid(key, list())
        if save_num >= 0 or key == Key.backspace:
            return 'restart'
        return ''
