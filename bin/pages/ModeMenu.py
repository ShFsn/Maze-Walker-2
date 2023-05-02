from bin.pages.Page import Page


class ModeMenu(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Select Game Mode:\n'
                             '[1] Single (1 player)\n'
                             '[2] Coop (2 players)\n'
                             '[3] Net Coop (2 players over local network)\n'
                             '[4] Show Scores table')
        self.contents.append('Press [Backspace] to go back')

    def action(self, key, maze):
        super().action(key, maze)
        if key == '1':
            maze.set_single()
        elif key == '2':
            maze.set_multi()
        elif key == '3':
            maze.set_multi()
            maze.set_online()

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        elif key == '1':
            return 'MazeTypeMenu'
        elif key == '2':
            return 'MazeTypeMenu'
        elif key == '3':
            return 'HostModeMenu'
        elif key == '4':
            return 'ScoresTable'
        return ''
