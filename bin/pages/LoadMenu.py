from bin.pages.SavesMenu import SavesMenu


class LoadMenu(SavesMenu):
    def __init__(self):
        super().__init__()
        self.contents.append('Press [Backspace] to go back')
        self._saves = list()

    def get_contents(self, maze):
        if self._showed:
            return tuple()
        super().get_contents(maze)
        path = 'saves/' + ('single/' if maze.is_single() else 'multi/') + 'save_'
        self._saves = list()
        for i in range(5):
            with open(path + str(i + 1)) as f_in:
                self._saves.append(f_in.read())
            self.contents[0] += ('[' if len(self._saves[i]) else ' ') + str(i + 1) + (
                ']' if len(self._saves[i]) else ' ')
            self.contents[0] += ' Save ' + str(i + 1) + '\n'
        self._showed = True
        return tuple(self.contents)

    def _assert_valid(self, key, saves):
        save_num = super()._assert_valid(key, self._saves)
        if save_num < 0:
            return save_num
        if not len(self._saves[save_num]):
            return -1
        return save_num

    def action(self, key, maze):
        super().action(key, maze)
        save_num = self._assert_valid(key, self._saves)
        if save_num < 0:
            return
        save_num = int(key) - 1
        maze.set_data(self._saves[save_num])

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        save_num = self._assert_valid(key, self._saves)
        if save_num < 0:
            return ''
        return 'GamePage'
