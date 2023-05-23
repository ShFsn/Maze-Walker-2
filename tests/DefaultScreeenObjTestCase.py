import unittest
from bin.ScreenObj import ScreenObj


class DefaultScreenObjTestCase(unittest.TestCase):
    def setUp(self):
        self.screen_obj = ScreenObj()
        with open('../data/Title_art', 'r') as f:
            self.obj_test = f.read()
        self.screen_obj.set_obj(self.obj_test)

    def test_get_size(self):
        self.assertEqual(self.screen_obj.get_size(), (57, 8), 'incorrect object size')

    def test_next_line(self):
        for i in self.obj_test.split('\n'):
            self.assertEqual(self.screen_obj.next_line(), i, 'incorrect thrown line')


if __name__ == '__main__':
    unittest.main(argv=['', ], defaultTest='DefaultWidgetSizeTestCase', exit=False)
