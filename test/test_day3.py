import numpy as np
import unittest
from day3 import rectangle, place_rectangle_on_fabric, count_overlap

class Test(unittest.TestCase):

    def test_parse_square(self):
        target = '#12 @ 604,670: 22x16'

        expected = rectangle(12, 604, 670, 22, 16)
        actual = rectangle.from_str(target)

        print(expected)
        print(actual)

        assert expected == actual

    def test_place_rectangle_on_fabric(self):

        target = rectangle(1, 2, 1, 2, 2)
        fabric = np.zeros([4, 4])
 
        expected = np.array([[0, 0, 0, 0],
                             [0, 0, 1, 1],
                             [0, 0, 1, 1],
                             [0, 0, 0, 0]])
        actual = place_rectangle_on_fabric(target, fabric)

        assert (expected == actual).all()

    def test_place_rectangle_on_fabric_twice(self):

        target = rectangle(1, 1, 1, 2, 2)
        fabric = np.zeros([4, 4])
 
        expected = np.array([[0, 0, 0, 0],
                             [0, 2, 2, 0],
                             [0, 2, 2, 0],
                             [0, 0, 0, 0]])
        fabric = place_rectangle_on_fabric(target, fabric)
        actual = place_rectangle_on_fabric(target, fabric)

        assert (expected == actual).all()

    def test_count_overlap(self):

        target = np.array([[0, 0, 0, 0],
                           [0, 2, 2, 0],
                           [0, 1, 1, 0],
                           [0, 0, 0, 0]])
        expected = 2
        actual = count_overlap(target)

        assert expected == actual
