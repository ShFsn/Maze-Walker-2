from bin.pages.Page import Page


class MazeTypeMenu(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Would You like to:\n'
                             '[1] Generate a new maze (DFS)\n'
                             '[2] Generate a new maze (MST)\n'
                             '[3] Load saved one')
        self.contents.append('Press [Backspace] to go back')

    def action(self, key, maze):
        if key == '1':
            maze.set_generator('DFS')
        elif key == '2':
            maze.set_generator('MST')

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        elif key == '1':
            return 'SizeSelect'
        elif key == '2':
            return 'SizeSelect'
        elif key == '3':
            return 'LoadMenu'
        return ''
