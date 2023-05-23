from bin.ScreenObj import ScreenObj
import sys


class Screen:
    def __init__(self):
        (self._win_w, self._win_h) = self.get_win_size()
        self._draw_pool = tuple()
        self._redraw = True

    @staticmethod
    def get_win_size():
        import shutil
        return shutil.get_terminal_size()  # pass fallback
        # os.terminal_size(columns=87, lines=23)  # returns a named-tuple

    def _update_win_size(self):
        pass
        _win_w, _win_h = self._win_w, self._win_h
        (self._win_w, self._win_h) = self.get_win_size()
        if _win_w != self._win_w or _win_h != self._win_h:
            self._redraw = True

    def refresh(self, draw_pool=tuple()):
        self._update_win_size()
        if len(draw_pool) > 0:
            self._draw_pool = draw_pool
            self._redraw = True
        if self._redraw:
            # update image
            self._draw(self._draw_pool)
        else:
            # do not update image to prevent overload
            pass
        self._redraw = False

    def _draw(self, draw_pool):
        objs = list()
        sum_height = 0
        max_width = 0
        for i in draw_pool:
            obj = ScreenObj()
            obj.set_obj(i)
            objs.append(obj)
            max_width = obj.get_size()[0] if obj.get_size()[0] > max_width else max_width
            sum_height += obj.get_size()[1]
        if max_width + 2 > self._win_w or sum_height + len(objs) + 1 > self._win_h:
            objs = list()
            obj = ScreenObj()
            obj.set_obj('Window size\nis too small')
            objs.append(obj)
            sum_height = obj.get_size()[1]
        output = self._compose(objs, sum_height)
        print(output, end='')
        sys.stdout.flush()

    def _compose(self, objs, sum_height):
        output = ''
        space_height = (self._win_h - sum_height) // (len(objs) + 1)
        for obj in objs:
            output += '\n' * space_height
            for i in range(obj.get_size()[1]):
                output += '\n' + ' ' * ((self._win_w - obj.get_size()[0]) // 2) + obj.next_line()
        space_height = self._win_h - sum_height - space_height * len(objs)
        output += '\n' * space_height
        return output
