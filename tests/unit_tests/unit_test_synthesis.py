from src.synthesis.handwriting_reconstruction import generate_bsplain
from src.synthesis.control_points import find_neighbours, is_neighbour_pixel, points_distance, remove_edge
import unittest


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


if __name__ == '__main__':
    unittest.main()