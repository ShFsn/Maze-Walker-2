import bin.pages.Page as Page


class TitleScreen(Page.Page):
    def __init__(self):
        super().__init__()
        with open('data/Title_art.txt', 'r') as f_in:
            self.contents.append(f_in.read())
        self.contents.append('Press any key to start!\n'
                             '   Press ESC to exit')

    def get_next_state(self, key):
        if key != '':
            return 'StartMenu'
        return ''
