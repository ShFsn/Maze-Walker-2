class Player:
    def __init__(self):
        self._active = False
        self._position = (0, 0)
        self._letter = ''

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def set_letter(self, letter):
        self._letter = letter

    def get_letter(self):
        return self._letter

    def set_pos(self, x, y):
        self._position = (x, y)

    def get_pos(self):
        return self._position
