
from src.file_handler.file_handler import get_absolute_path
from src.synthesis.handwriting_reconstruction import draw_letter, generate_bsplain, generate_bsplain_fig
from src.synthesis.control_points import find_neighbours, is_neighbour_pixel, points_distance, remove_edge
import matplotlib.pyplot as plt
import unittest
from unittest.mock import Mock

# ------------ get_sequences_extended.py ------------
from src.synthesis.get_sequences_extended import compare_points
from src.synthesis.get_sequences_extended import get_points
from src.synthesis.get_sequences_extended import find_non_zero_occurence_point
from src.synthesis.get_sequences_extended import find_single_occurence_point

# ------------ generate_letter.py ------------
from src.synthesis.generate_letter import dist
from src.synthesis.generate_letter import mid_point
from src.synthesis.generate_letter import get_shift
from src.synthesis.generate_letter import shift_points

# ------------ generate_letter.py ------------
from src.synthesis.control_points import check_sequences
from src.synthesis.control_points import left_only_control_points
from src.synthesis.control_points import match_points


class SynthesisUnitTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Synthesis Unit Tests')
        cls.p1 = (0, 0)
        cls.p2 = (0, 1)
        cls.p3 = (3, 0)
        cls.edges = set()
        cls.edges.add((cls.p1, cls.p2))
        cls.edges.add((cls.p2, cls.p3))
        cls.edges2 = (((39, 3), (40, 3)), ((19, 12), (20, 12)), ((17, 14), (18, 13)), ((16, 14), (17, 14)), ((9, 19), (10, 19)), ((22, 11), (23, 10)), ((33, 5), (34, 4)), ((38, 3), (39, 3)), ((21, 11), (22, 11)), ((44, 2), (45, 2)), ((49, 6), (49, 7)), ((26, 8), (27, 8)), ((49, 7), (49, 8)), ((37, 3), (38, 3)), ((47, 3), (48, 4)), ((48, 15), (48, 16)), ((34, 4), (35, 4)), ((46, 19), (46, 20)), ((35, 4), (36, 4)), ((18, 13), (19, 12)), ((25, 9), (26, 8)), ((4, 24), (5, 23)), ((48, 4), (49, 5)), ((36, 4), (37, 3)), ((41, 3), (42, 2)), ((49, 9), (49, 10)), ((14, 16), (15, 15)), ((13, 17), (14, 16)), ((45, 2), (46, 3)), ((48, 12), (48, 13)), ((12, 17), (13, 17)), ((31, 6), (32, 5)), ((47, 17), (47, 18)), ((15, 15), (16, 14)), ((48, 12), (49, 11)), ((
            43, 2), (44, 2)), ((43, 25), (43, 26)), ((48, 13), (48, 14)), ((7, 21), (8, 20)), ((27, 8), (28, 8)), ((24, 9), (25, 9)), ((28, 8), (29, 7)), ((23, 10), (24, 9)), ((46, 19), (47, 18)), ((8, 20), (9, 19)), ((6, 22), (7, 21)), ((29, 7), (30, 6)), ((47, 17), (48, 16)), ((5, 23), (6, 22)), ((11, 18), (12, 17)), ((30, 6), (31, 6)), ((41, 28), (42, 27)), ((42, 27), (43, 26)), ((44, 23), (44, 24)), ((40, 3), (41, 3)), ((1, 26), (2, 25)), ((10, 19), (11, 18)), ((32, 5), (33, 5)), ((42, 2), (43, 2)), ((45, 21), (45, 22)), ((49, 5), (49, 6)), ((49, 8), (49, 9)), ((49, 10), (49, 11)), ((48, 14), (48, 15)), ((2, 25), (3, 24)), ((45, 21), (46, 20)), ((46, 3), (47, 3)), ((44, 23), (45, 22)), ((3, 24), (4, 24)), ((43, 25), (44, 24)), ((20, 12), (21, 11)))

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Synthesis Unit Tests')

    @classmethod
    def setUp(cls):
        """ before each test """
        cls.edges.clear()
        cls.edges.add((cls.p1, cls.p2))
        cls.edges.add((cls.p2, cls.p3))

    def test_is_neighbour_pixel(self):
        self.assertTrue(is_neighbour_pixel(self.p1, self.p2))
        self.assertFalse(is_neighbour_pixel(self.p1, self.p3))

    def test_points_distance(self):
        self.assertEqual(points_distance(self.p1, self.p2), 1)
        self.assertEqual(points_distance(self.p1, self.p3), 3)

    def test_find_neighbours(self):
        result1 = find_neighbours(self.p1, self.edges)
        self.assertEqual(len(result1), 1)
        self.assertIn(self.p2, result1)
        result1 = find_neighbours(self.p2, self.edges)
        self.assertEqual(len(result1), 2)
        self.assertIn(self.p1, result1)
        self.assertIn(self.p3, result1)

    def test_remove_edge(self):
        self.assertTrue(len(self.edges) == 2)
        remove_edge(self.edges, self.p1, self.p2)
        self.assertTrue(len(self.edges) == 1)
        remove_edge(self.edges, self.p1, self.p2)
        self.assertTrue(len(self.edges) == 1)

    def test_generate_bsplain(self):
        x = [1, 2, 3]
        y = [3, 4, 5]
        result = generate_bsplain(x, y)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 2)

    def test_generate_bsplain_fig(self):
        letter = [[(1, 1), (-1, -1)], [(0, 0), (0, 4), (0, 7)], [(-10, -10)]]
        result = generate_bsplain_fig(
            letter, image_size=(20, 20), offset_x=3, offset_y=-3, show_points_flag=True)
        self.assertIsNotNone(result)

    def test_draw_letter(self):
        letter = [[(1, 1), (-1, -1)], [(0, 0), (0, 4), (0, 7)], [(-1, -2)]]
        path = get_absolute_path('./tests/data/output/draw_letter_test.png')
        result = draw_letter(letter, show_flag=False,
                             skeleton_flag=True, path_to_save_file=path)
        self.assertIsNotNone(result)
        plot = plt
        plot.show = Mock()
        result = draw_letter(letter, show_flag=True,
                             skeleton_flag=False)
        self.assertIsNotNone(result)

    # ------------ get_sequences_extended.py ------------

    def test_compare_points(self):
        self.assertTrue(compare_points([14, 1], [14, 1]))
        self.assertFalse(compare_points([1, 14], [14, 1]))

    def test_find_non_zero_occurence_point(self):
        points = get_points(self.edges2)
        index = 14
        for i in points:
            i[1] = 0
        points[index][1] = 1

        self.assertEqual(find_non_zero_occurence_point(points), index)

    def test_find_single_occurence_point(self):
        points = get_points(self.edges2)
        index = 14
        for i in points:
            i[1] = 10
        points[index][1] = 1

        self.assertEqual(find_single_occurence_point(points), index)

    # ------------ generate letters.py ------------

    def test_dist(self):
        a1 = 10
        a2 = 20
        b1 = 15
        b2 = 6
        tuple1 = (a1, b1)
        tuple2 = (a2, b2)
        result = 13
        self.assertEqual(dist(tuple1, tuple2), result)

        a1 = 0
        a2 = 0
        b1 = 0
        b2 = 0
        tuple1 = (a1, b1)
        tuple2 = (a2, b2)
        result = 0
        self.assertEqual(dist(tuple1, tuple2), result)

    def test_mid_point(self):
        a1 = 10
        a2 = 20
        b1 = 15
        b2 = 6
        tuple1 = (a1, b1)
        tuple2 = (a2, b2)
        result = mid_point(tuple1, tuple2)
        self.assertGreater(result[0], 13.5)
        self.assertLess(result[0], 18)
        self.assertGreater(result[1], 9)
        self.assertLess(result[1], 12)

        a1 = 0
        a2 = 0
        b1 = 0
        b2 = 0
        tuple1 = (a1, b1)
        tuple2 = (a2, b2)
        result = mid_point(tuple1, tuple2)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)

    def test_get_shift(self):
        l1 = []
        l1.append((5, 0))
        l1.append((120, 89))
        l1.append((1, 14))
        l1.append((12, -9))
        l1.append((10, 4))
        l1.append((5, 5))
        l2 = []
        l2.append((1, 1))
        l2.append((-56, 22))
        l2.append((13, 14))
        l2.append((0, 7))
        l2.append((-1, -3))
        l2.append((13, 45))
        result = (-30, -3)
        self.assertEqual(get_shift(l1, l2), result)

        l1 = []
        l2 = []
        result = (0, 0)
        self.assertEqual(get_shift(l1, l2), result)

    def test_shifts_points(self):
        l1 = []
        m = (5, 10)
        l1.append((5, 0))
        l1.append((120, 89))
        l1.append((1, 14))
        l1.append((12, -9))
        l1.append((10, 4))
        l1.append((5, 5))
        l2 = []
        l2.append((5 - m[0], 0 - m[1]))
        l2.append((120 - m[0], 89 - m[1]))
        l2.append((1 - m[0], 14 - m[1]))
        l2.append((12 - m[0], -9 - m[1]))
        l2.append((10 - m[0], 4 - m[1]))
        l2.append((5 - m[0], 5 - m[1]))
        result = shift_points(l1, m)
        for i in range(len(l1)):
            self.assertEqual(result[i], l2[i])

        l1 = []
        m = (0, 0)
        l1.append((0, 0))
        l1.append((0, 0))
        result = shift_points(l1, m)
        for i in range(len(l1)):
            self.assertEqual(result[i], (0, 0))

# ------------ generate_letter.py ------------

    def test_check_sequences(self):
        test_seq = [[(2, 1), (1, 2), (2, 1)], [(3, 2), (4, 2)]]
        result = check_sequences(test_seq)
        print('NOWEADSDSDAD')
        print(result)
        self.assertEqual(len(result[0]), len(test_seq[0]))
        self.assertEqual(len(result[1]), len(test_seq[1]))

        test_seq = [[(2, 1), (1, 2), (2, 1), (2, 1)], [(3, 2), (4, 2)]]
        result = check_sequences(test_seq)
        self.assertEqual(len(result[0]), len(test_seq[0]) - 1)
        self.assertEqual(len(result[1]), len(test_seq[1]))

    def test_left_only_control_points(self):
        test_seq = [[(2, 1), (1, 2), (2, 1)], [(3, 2), (4, 2)]]
        cp = []
        result = left_only_control_points(test_seq, cp)
        self.assertEqual(len(result), len(test_seq))

        test_seq = [[(2, 1), (1, 2), (2, 1), (2, 1)], [(3, 2), (4, 2)]]
        cp = [(2, 1)]
        result = left_only_control_points(test_seq, cp)
        self.assertEqual(len(result[0]), len(test_seq[0]))

    def test_match_points(self):
        test_seq = [[(2, 1), (1, 2), (2, 1)], [(3, 2), (4, 2)]]
        new_letter = [[(1, 2), (3, 2)]]
        result = match_points(test_seq, new_letter)
        self.assertEqual(len(result[0]), 1)


if __name__ == '__main__':
    unittest.main()
