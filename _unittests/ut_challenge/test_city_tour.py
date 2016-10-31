#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


from pyquickhelper.loghelper import fLOG
from src.ensae_projects.challenge.city_tour import distance_solution, SolutionException, haversine_distance, euler_path


class TestCityTour(unittest.TestCase):

    def test_solution1(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index = [1, 2, 3, 4]
        edges = [[0, 1], [1, 2], [2, 3], [3, 0]]
        distances = [1, 1, 1, 1]
        solution = [1, 2, 3, 4]
        try:
            distance_solution(edges_index, edges, distances, [1, 2])
        except SolutionException as e:
            assert "Did you cover" in str(e)
        try:
            distance_solution(edges_index, edges, distances, [1, 2, 2, 2])
        except SolutionException as e:
            assert "Did you cover" in str(e)
        try:
            distance_solution(edges_index, edges, distances, [1, 2, 3, 0])
        except SolutionException as e:
            assert "is not in edges_index" in str(e)
        d = distance_solution(edges_index, edges, distances, solution)
        self.assertEqual(d, 4)

    def test_haversine(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        a1, b1 = -122.34991548199997, 47.46763155800005
        a2, b2 = -122.34991155699998, 47.468532819000075
        d = haversine_distance(a1, b1, a2, b2)
        self.assertEqual(d, 0.053626018369778275)

    def test_solution2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index = [1, 2, 3, 4, 5, 6]
        edges = [[0, 1], [1, 2], [2, 3], [3, 0],
                 [0, 5], [5, 1], [2, 6], [3, 6]]
        distances = [1, 1, 1, 1, 1, 1]
        solution = [1, 2, 3, 4, 5, 6]
        try:
            distance_solution(edges_index, edges, distances, solution)
        except SolutionException as e:
            assert "Are you sure?" in str(e)
        solution = [1, 2, 3, 4, 5, 6, 1, 2]
        d = distance_solution(edges_index, edges, distances, solution)
        self.assertEqual(d, len(solution))

    def test_eulerian(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index = [1, 2, 3, 4]
        edges = [[0, 1], [1, 2], [2, 3], [3, 0]]
        distances = [1, 1, 1, 1]
        solution = [1, 2, 3, 4]
        d = distance_solution(edges_index, edges, distances, solution)
        path = euler_path(edges_index, edges, solution)
        self.assertEqual(len(path), d)
        self.assertEqual(list(sorted((path))), [1, 2, 3, 4])

    def test_eulerian2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index = [1, 2, 3, 4, 5, 6]
        edges = [[0, 1], [1, 2], [2, 3], [3, 0],
                 [0, 5], [5, 1], [2, 6], [3, 6]]
        distances = [1, 1, 1, 1, 1, 1]
        solution = [1, 2, 3, 4, 5, 6, 1, 2]
        try:
            distance_solution(edges_index, edges, distances, solution)
        except SolutionException as e:
            if "Some vertices have an odd degree" not in str(e):
                raise e
        solution = [1, 2, 3, 4, 5, 6, 1, 2, 2]
        d = distance_solution(edges_index, edges, distances, solution)
        path = euler_path(edges_index, edges, solution)
        self.assertEqual(len(path), d)
        self.assertEqual(list(sorted(path)), [1, 1, 2, 2, 2, 3, 4, 5, 6])

    def test_euler_path_incomplete(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index = [0, 4994, 11394, 9989, 1670, 11274, 17680, 3353, 9118, 30370, 15023,
                       6712, 8378, 29114, 4553, 1101, 6488, 107, 1003, 12783, 2418, 2803, 2808, 6265]
        solution = [0, 4994, 11394, 9989, 1670, 11274, 17680, 3353, 9118, 30370, 15023, 6712, 8378, 29114, 4553,
                    1101, 6488, 107, 1003, 12783, 2418, 2803, 2808, 6265, 17680, 30370, 12783, 0, 3353, 9118, 8378, 15023]
        edges = [(10, 7), (5, 4), (4, 0), (10, 11), (9, 10), (7, 2), (17, 16), (5, 1), (11, 5), (17, 13), (16, 15), (14, 4),
                 (15, 11), (1, 0), (4, 6), (8, 9), (13, 9), (7, 5), (11, 14), (16, 10), (2, 1), (12, 8), (9, 3), (12, 13)]
        asso = {edges_index[i]: edges[i] for i in range(len(edges_index))}
        for i in range(0, 20):
            path = euler_path(edges_index, edges, solution)
            assert len(path) > 0
            self.assertEqual(list(sorted(path)), list(sorted(solution)))
            for i in range(1, len(path)):
                ed = path[i - 1:i + 1]
                e1 = asso[ed[0]]
                e2 = asso[ed[1]]
                con = 0
                if e1[0] in e2 or e1[1] in e2:
                    con += 1
                if e2[0] in e1 or e2[1] in e1:
                    con += 1
                if con == 0:
                    raise Exception(
                        "inonsistency:\npath={0}\ned={1}\ne1={2}, e2={3}".format(path, ed, e1, e2))


if __name__ == "__main__":
    unittest.main()
