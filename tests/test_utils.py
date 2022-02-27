import unittest

from myConvexHull.utils import vec_len, det, dist_to_line

class TestConvexHullLibrary(unittest.TestCase):
    def test_vec_len(self):
        self.assertEqual(vec_len((0, 0)), 0)
        self.assertEqual(vec_len((1, 0)), 1)
        self.assertEqual(vec_len((0, 1)), 1)
        self.assertAlmostEqual(vec_len((1, 1)), 1.4142135623730)
        self.assertAlmostEqual(vec_len((-1, 1)), 1.4142135623730)
        self.assertAlmostEqual(vec_len((-1, 2)), 2.2360679774997)
        self.assertAlmostEqual(vec_len((5, 10)), 11.180339887498)
        self.assertAlmostEqual(vec_len((-6, -8)), 10)

    def test_det(self):
        self.assertAlmostEqual(det(((4.3,3.0), (4.6,3.6)), (4.4,3.2)), 0)
        self.assertAlmostEqual(det(((4.3,3.0), (4.6,3.6)), (4.4,3.5)), 0.09)
        self.assertAlmostEqual(det(((1,2), (3,5)), (2,3)), -1)

    def test_dist_to_line(self):
        self.assertAlmostEqual(dist_to_line(((4.3,3.0), (4.6,3.6)), (4.4,3.2)), 0)
        self.assertAlmostEqual(dist_to_line(((4.3,3.0), (4.6,3.6)), (4.4,3.5)), 0.134164078649987)
        self.assertAlmostEqual(dist_to_line(((1,2), (3,5)), (2,3)), 0.2773500981126)

if __name__ == '__main__':
    unittest.main()