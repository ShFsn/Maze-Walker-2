from bin.pages.Page import Page


class HostModeMenu(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Select Online Mode:\n'
                             '[1] Host\n'
                             '[2] Guest')
        self.contents.append('Press [Backspace] to go back')

    def action(self, key, maze):
        super().action(key, maze)
        if key == '1':
            maze.set_host()
        elif key == '2':
            maze.set_guest()

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        elif key == '1':
            return 'HostWait'
        elif key == '2':
            return 'HostSelect'
        return ''
