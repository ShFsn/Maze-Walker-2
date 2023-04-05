class ScreenObj:
    def __init__(self):
        self._width = 0
        self._height = 0
        self._line = 0
        self._contents = list()

    def set_obj(self, obj):
        for i in obj.split('\n'):
            self._height += 1
            self._width = len(i) if len(i) > self._width else self._width
            self._contents.append(i)

    def next_line(self):
        line = self._contents[self._line] if self._line < self._height else ''
        self._line += 1
        return line

    def get_size(self):
        return self._width, self._height
