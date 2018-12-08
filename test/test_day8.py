from Day8 import recursive_read_1, recursive_read_2
import queue
import unittest

class Test(unittest.TestCase):

    def test_recursive_read_1(self):
        num_quque = queue.Queue()

        nums = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
        for num in nums:
            num_quque.put(num)

        expected = 138
        actual = recursive_read_1(num_quque)

        assert expected == actual

    def test_recursive_read_2(self):
        num_quque = queue.Queue()

        nums = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
        for num in nums:
            num_quque.put(num)

        expected = 66
        actual = recursive_read_2(num_quque)

        assert expected == actual
