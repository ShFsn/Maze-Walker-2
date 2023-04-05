import bin.pages.Page as Page


class StartMenu(Page.Page):
    def __init__(self):
        super().__init__()
        self.contents.append('Would You like to:\n'
                             '[1] Generate a new maze\n'
                             '[2] Load saved one')
        self.contents.append('Press Backspace to go back')

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        return ''
