from bin.pages.Page import Page


class TitleScreen(Page):
    def __init__(self):
        super().__init__()
        with open('data/Title_art', 'r') as f_in:
            self.contents.append(f_in.read())
        self.contents.append('Press [ANY] key to start!\n'
                             '   Press [ESC] to exit')

    def get_next_state(self, key):
        if key != '':
            return 'ModeMenu'
        return ''
