from bin.pages.Page import Page


class PointsPosSelect(Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Select position of start and finish points:\n\n')
        with open('data/PointsPosArt', 'r') as f:
            self.contents[0] += f.read()
        self.contents.append('Press [Backspace] to go back')

    def action(self, key, maze):
        super().action(key, maze)
        if key == '1' or key == '2' or key == '3':
            maze.set_points_pos_type(int(key))
            maze.generate()
            if maze.is_online():
                maze.set_mp_maze(maze.get_data())

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        elif key == '1':
            return 'GamePage'
        elif key == '2':
            return 'GamePage'
        elif key == '3':
            return 'GamePage'
        return ''
