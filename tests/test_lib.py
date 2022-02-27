import unittest

from scipy.spatial import ConvexHull
from sklearn import datasets

from myConvexHull.lib import LinearSeparabilityDataset

class TestConvexHullLibrary(unittest.TestCase):
    def assertSequence(self, l1: list, l2: list, cond: lambda x, y: x == y) -> bool:
        """Check if two list of sequence is the same.

        It will make sure every sequence is the same on both list,
        regardless the order of the sequence's element,
        or the order of the sequence itself.

        Args:
            l1 (list): List of lines 1.
            l2 (list): List of lines 2.

        Returns:
            bool: True if both list match the condition.
        """
        if len(l1) != len(l2):
            self.fail(f'Length of list is different: {len(l1)} vs {len(l2)}')
        for i in range(len(l1)):
            valid = False
            for j in range(len(l2)):
                valid = cond(
                    l1[i], l2[j]
                )
                if valid:
                    break
            if not valid:
                self.fail(f'Line {l1[i]} not found in {l2}')

    def test_convex_hull(self):
        """Test to compare the result of custom convex hull implementation
        vs scipy's convex hull implementation.
        """
        t = tuple
        cond = lambda u, v: lambda x, y: all([
            t(u[x[i]]) == t(v[y[i]])
            or t(u[x[::-1][i]]) == t(v[y[i]])
            for i in range(2)
        ])
        cond2 = lambda u, v: lambda x, y: t(u[x]) == t(v[y])
        for dname in ['iris', 'wine', 'breast_cancer']:
            data = getattr(datasets, f'load_{dname}')(as_frame=True)
            vis = {
                'a': LinearSeparabilityDataset(
                    frame=data.frame,
                    target_names=data.target_names,
                ),
                'b': LinearSeparabilityDataset(
                    frame=data.frame,
                    target_names=data.target_names,
                    backend=ConvexHull
                ),
            }
            ft_len = len(vis['a'].feature_names)
            for i in range(ft_len - 1):
                print(f'Comparing {dname} on {vis["a"].feature_names[i]} vs {vis["b"].feature_names[i+1]}')
                c = {
                    'a': vis['a'].getConvex(i, i+1),
                    'b': vis['b'].getConvex(i, i+1),
                }
                for j in range(len(c['a'])):
                    self.assertSequence(
                        c['a'][j].simplices,
                        c['b'][j].simplices,
                        cond(c['a'][j].points, c['b'][j].points)
                    )
                    self.assertSequence(
                        c['a'][j].vertices,
                        c['b'][j].vertices,
                        cond2(c['a'][j].points, c['b'][j].points)
                    )

if __name__ == '__main__':
    unittest.main()