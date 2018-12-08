from Day6 import Point, Rectangle, find_bounds, find_index_of_closest_target, find_indices_of_infinite_area_targets, find_largest_area, find_safe_area
import unittest

class Test(unittest.TestCase):

    def get_example_targets(self):
        targets = []
        targets.append(Point(1, 1))
        targets.append(Point(1, 6))
        targets.append(Point(8, 3))
        targets.append(Point(3, 4))
        targets.append(Point(5, 5))
        targets.append(Point(8, 9))

        return targets

    def test_point_from_str(self):
        input_data = '268, 273'

        expected = Point(268, 273)
        actual = Point.from_str(input_data)

        assert expected == actual

    def test_find_bounds(self):
        expected = Rectangle(top=1, left=1, bottom=9, right=8)
        actual = find_bounds(self.get_example_targets())

        assert expected == actual

    def test_find_index_of_closest_target(self):
        input_data = Point(0, 0)
        expected = 0

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        assert expected == actual

    def test_find_index_of_closest_target_coincidence(self):
        input_data = Point(1, 1)
        expected = -1

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        assert expected == actual

    def test_find_index_of_closest_target_4_4(self):
        input_data = Point(4,4)
        expected = 3

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        print(actual)
        assert expected == actual


    def test_find_index_of_closest_target_5_4(self):
        input_data = Point(5,4)
        expected = 4

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        assert expected == actual

    def test_find_index_of_closest_target_equidistant(self):
        input_data = Point(5, 0)
        expected = -1

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        assert expected == actual

    def test_find_index_of_closest_target_zero(self):
        input_data = Point(1, 1)
        expected = -1

        targets = self.get_example_targets()
        actual = find_index_of_closest_target(targets, input_data)

        assert expected == actual

    def test_find_infinite_indices(self):
        expected = {0, 1, 2, 5}
        actual = find_indices_of_infinite_area_targets(self.get_example_targets())

        assert expected == actual

    def test_find_largest_area(self):
        targets = self.get_example_targets()
        indices_of_infinite_area_targets = find_indices_of_infinite_area_targets(targets)

        expected = 17
        actual = find_largest_area(targets, indices_of_infinite_area_targets)
        print(actual)
        assert expected == actual

    def test_find_safe_aera(self):
        targets = self.get_example_targets()
        safe_threshold = 32

        expected = 16
        actual = find_safe_area(targets, safe_threshold)
        print(actual)
        assert expected == actual
