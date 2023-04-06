from bin.pages.Page import Page
from pynput.keyboard import Key
import string


class SavesMenu(Page):
    def __init__(self):
        super().__init__()
        self._check_saves()

    def get_next_state(self, key):
        res = super().get_next_state(key)
        if res != '':
            return res
        return ''

    # noinspection PyBroadException
    @staticmethod
    def _check_saves():
        import os
        try:
            os.chdir('saves')
        except:
            os.mkdir('saves')
            os.chdir('saves')
        try:
            os.chdir('single')
        except:
            os.mkdir('single')
            os.chdir('single')
        for i in range(5):
            try:
                f = open('save_' + str(i+1), 'r')
                f.close()
            except:
                f = open('save_' + str(i+1), 'w')
                f.close()
        os.chdir('..')
        try:
            os.chdir('multi')
        except:
            os.mkdir('multi')
            os.chdir('multi')
        for i in range(5):
            try:
                f = open('save_' + str(i+1), 'r')
                f.close()
            except:
                f = open('save_' + str(i+1), 'w')
                f.close()
        os.chdir('../..')

    def _assert_valid(self, key, saves):
        if type(key) == Key:
            return -1
        if key not in string.digits or key == '':
            return -1
        save_num = int(key) - 1
        if save_num < 0 or save_num > 4:
            return -1
        return save_num
