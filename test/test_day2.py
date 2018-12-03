import unittest
from Day2 import build_dict, check_repeat_n, remove_letter_n

class Test(unittest.TestCase):
    def test_build_dict(self):
        target = 'bababc'
        expected = {'b': 3, 'a': 2, 'c' : 1}
    
        actual = build_dict(target)

        self.assertDictEqual(expected, actual)

    def test_check_repeat_two(self):
        target = {'b': 3, 'a': 2, 'c' : 1}

        expected = True
        actual = check_repeat_n(target, 2)

        assert expected == actual

    def test_remove_letter_n_0(self):
        target = 'abcde'
        expected = 'bcde'

        actual = remove_letter_n(target, 0)
        assert expected == actual

    def test_remove_letter_n_n(self):
        target = 'abcde'
        expected = 'abcd'

        actual = remove_letter_n(target, 4)
        assert expected == actual

    def test_remove_letter_n_1(self):
        target = 'abcde'
        expected = 'acde'

        actual = remove_letter_n(target, 1)
        assert expected == actual
