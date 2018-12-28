from day5 import check_if_should_eliminate, do_reduce_loop
import unittest

class Test(unittest.TestCase):

    def test_check_if_should_eliminate(self):
        target = 'aA'
        expected = True
        actual = check_if_should_eliminate(target[0], target[1])

        assert expected == actual

    def test_check_if_should_eliminate_reverse(self):
        target = 'Aa'
        expected = True
        actual = check_if_should_eliminate(target[0], target[1])

        assert expected == actual

    def test_ex_1(self):
        target = 'abBA'

        expected = 0
        actual = len(do_reduce_loop(target))

        assert expected == actual

    def test_ex_2(self):
        target = 'abAB'

        expected = 4
        actual = len(do_reduce_loop(target))

        assert expected == actual

    def test_ex_3(self):
        target = 'aabAAB'

        expected = 6
        actual = len(do_reduce_loop(target))

        assert expected == actual

    def test_ex43(self):
        target = 'dabAcCaCBAcCcaDA'

        expected = 10
        actual = len(do_reduce_loop(target))

        assert expected == actual
