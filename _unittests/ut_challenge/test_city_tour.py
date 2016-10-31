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
from src.ensae_projects.challenge.city_tour import distance_solution, SolutionException


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


if __name__ == "__main__":
    unittest.main()
