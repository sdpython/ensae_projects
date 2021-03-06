# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from ensae_projects.challenge.city_tour import distance_solution, SolutionException, haversine_distance, euler_path
from ensae_projects.challenge.city_tour import distance_vertices, bellman_distances, compute_degrees, dijkstra_path
from ensae_projects.challenge.city_tour import matching_vertices, best_euler_path


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
        path = euler_path(edges_index, edges,  # pylint: disable=W0621
                          solution)
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
        path = euler_path(edges_index, edges,  # pylint: disable=W0621
                          solution)
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
            path = euler_path(edges_index, edges,  # pylint: disable=W0621
                              solution)
            assert len(path) > 0
            self.assertEqual(list(sorted(path)), list(sorted(solution)))
            for ii in range(1, len(path)):
                ed = path[ii - 1:ii + 1]
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

    def test_distance_djikstras(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        vertices = [(-122.34991548199997, 47.46763155800005), (-122.34991155699998, 47.468532819000075),
                    (-122.349907514, 47.469446668000046), (-122.34855159499995,
                                                           47.47036031400006),
                    (-122.34722154299999,
                     47.46765986400004), (-122.34721743899996, 47.46856001400005),
                    (-122.34721337199994,
                     47.466759281000066), (-122.34721334599999, 47.46946425100003),
                    (-122.34717558599999,
                     47.47218021800006), (-122.34695634299999, 47.47037913100007),
                    (-122.34651954599997,
                     47.46947199700003), (-122.34602084699998, 47.46857181000007),
                    (-122.34577976599996,
                     47.47219822000005), (-122.34577761299994, 47.470393184000045),
                    (-122.34552556999995,
                     47.46767758400006), (-122.34451462099997, 47.46858890800007),
                    (-122.34451260399999, 47.46949338600007), (-122.34451061099998, 47.47040481700003)]
        edges = [(10, 7), (5, 4), (4, 0), (10, 11), (9, 10), (7, 2), (17, 16), (5, 1),
                 (11, 5), (17, 13), (16, 15), (14, 4), (15, 11), (1, 0), (4, 6),
                 (8, 9), (13, 9), (7, 5), (11, 14), (16, 10), (2, 1), (12, 8),
                 (9, 3), (12, 13)]
        distances = [0.0006938432391730961, 0.0009001593555190061, 0.0026940877056109824, 0.0010290953928001187,
                     0.0010111922517731158, 0.0026942253755745885, 0.0009114331789785205, 0.002694255252624058, 0.001196650141037562,
                     0.0012670554031294153, 0.000904480248963228, 0.001696065569270049, 0.0015063230412799549,
                     0.0009012695466891699, 0.0009006200670015617, 0.0018143819538848289, 0.0011788137680839225,
                     0.0009042462633556375, 0.0010222227965844966, 0.0020070559761853316, 0.0009138579433356185, 0.001395936081803295,
                     0.0015953629752697774, 0.0018050372840282547]
        edges_index = [0, 4994, 11394, 9989, 1670, 11274, 17680, 3353, 9118, 30370, 15023,
                       6712, 8378, 29114, 4553, 1101, 6488, 107, 1003, 12783, 2418, 2803,
                       2808, 6265]
        assert edges_index
        dist = distance_vertices(edges, vertices, None)
        self.assertEqual(len(dist), len(edges))
        for d in dist:
            assert d is not None
        dist = bellman_distances(edges, distances)
        for (a, b), d in zip(edges, distances):
            self.assertEqual(dist[a, b], d)
        degrees = compute_degrees(edges)
        expected = len(degrees) ** 2 - len(degrees)
        self.assertEqual(len(dist), expected)
        odd = {k: v for k, v in degrees.items() if v % 2 != 0}
        self.assertEqual(odd, {16: 3, 1: 3, 3: 1, 6: 1, 7: 3, 13: 3})
        for va in odd:
            for vb in odd:
                if va != vb:
                    dij = dijkstra_path(edges, distances, va, vb)
                    jid = dijkstra_path(  # pylint: disable=W1114
                        edges, distances, vb, va)  # pylint: disable=W1114
                    jid2 = list(reversed(jid))
                    self.assertEqual(dij, jid2)
                    d1 = sum(distances[i] for i in dij)
                    d2 = dist[va, vb]
                    d3 = dist[vb, va]
                    m = min(d1, d2, d3)
                    delta = abs(m - max(d1, d2, d3))
                    r = delta / m
                    assert r < 1e-5

        odd_dist = {k: v for k, v in dist.items() if k[0] in odd and k[
            1] in odd}

        res = matching_vertices(odd_dist)
        res.sort()
        exp = [(1, 6), (3, 13), (7, 16)]
        self.assertEqual(res, exp)
        d1 = [odd_dist[p] for p in res]
        # fLOG(sum(d1), "details", d1)

        res = matching_vertices(odd_dist, algo="blossom")
        res.sort()
        exp = [(1, 6), (3, 13), (7, 16)]
        self.assertEqual(res, exp)
        d2 = [odd_dist[p] for p in res]
        # fLOG(sum(d2), "details", d2)
        assert sum(d2) <= sum(d1)

        res = matching_vertices(odd_dist, algo="basic")
        res.sort()
        exp = [(1, 3), (6, 7), (13, 16)]
        d3 = [odd_dist[p] for p in res]
        # fLOG(sum(d3), "details", d3)
        assert sum(d3) >= sum(d2)
        self.assertEqual(res, exp)

        exp = [(0, 1), (2, 7), (3, 9), (4, 6), (5, 10),
               (8, 12), (11, 14), (13, 17), (15, 16)]
        res = matching_vertices(dist, algo="blossom")
        res.sort()
        self.assertEqual(res, exp)

    def test_best_euler_path(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        vertices = [(-122.34991548199997, 47.46763155800005), (-122.34991155699998, 47.468532819000075),
                    (-122.349907514, 47.469446668000046), (-122.34855159499995,
                                                           47.47036031400006),
                    (-122.34722154299999,
                     47.46765986400004), (-122.34721743899996, 47.46856001400005),
                    (-122.34721337199994,
                     47.466759281000066), (-122.34721334599999, 47.46946425100003),
                    (-122.34717558599999,
                     47.47218021800006), (-122.34695634299999, 47.47037913100007),
                    (-122.34651954599997,
                     47.46947199700003), (-122.34602084699998, 47.46857181000007),
                    (-122.34577976599996,
                     47.47219822000005), (-122.34577761299994, 47.470393184000045),
                    (-122.34552556999995,
                     47.46767758400006), (-122.34451462099997, 47.46858890800007),
                    (-122.34451260399999, 47.46949338600007), (-122.34451061099998, 47.47040481700003)]
        edges = [(10, 7), (5, 4), (4, 0), (10, 11), (9, 10), (7, 2), (17, 16), (5, 1),
                 (11, 5), (17, 13), (16, 15), (14, 4), (15, 11), (1, 0), (4, 6),
                 (8, 9), (13, 9), (7, 5), (11, 14), (16, 10), (2, 1), (12, 8),
                 (9, 3), (12, 13)]
        distances = [0.0006938432391730961, 0.0009001593555190061, 0.0026940877056109824, 0.0010290953928001187,
                     0.0010111922517731158, 0.0026942253755745885, 0.0009114331789785205, 0.002694255252624058, 0.001196650141037562,
                     0.0012670554031294153, 0.000904480248963228, 0.001696065569270049, 0.0015063230412799549,
                     0.0009012695466891699, 0.0009006200670015617, 0.0018143819538848289, 0.0011788137680839225,
                     0.0009042462633556375, 0.0010222227965844966, 0.0020070559761853316, 0.0009138579433356185, 0.001395936081803295,
                     0.0015953629752697774, 0.0018050372840282547]
        edges_index = [0, 4994, 11394, 9989, 1670, 11274, 17680, 3353, 9118, 30370, 15023,
                       6712, 8378, 29114, 4553, 1101, 6488, 107, 1003, 12783, 2418, 2803,
                       2808, 6265]
        co, ind, d = best_euler_path(edges_index=edges_index, edges=edges,
                                     distances=distances, vertices=vertices, fLOG=fLOG)
        fLOG(co)
        fLOG("distance", d)
        co.sort()
        ind.sort()
        exp_ind = [0, 0, 107, 1003, 1101, 1670, 2418, 2803, 2808, 2808, 3353, 3353, 4553, 4553, 4994, 4994,
                   6265, 6488, 6488, 6712, 8378, 9118, 9989, 11274, 11394, 12783, 12783, 15023, 17680, 29114, 30370]
        self.assertEqual(ind, exp_ind)
        exp_co = [(1, 0), (2, 1), (4, 0), (4, 6), (4, 6), (5, 1), (5, 1), (5, 4), (5, 4), (7, 2),
                  (7, 5), (8, 9), (9, 3), (9, 3), (9, 10), (10, 7),
                  (10, 7), (10, 11), (11, 5), (11, 14), (12,
                                                         8), (12, 13), (13, 9), (13, 9), (14, 4),
                  (15, 11), (16, 10), (16, 10), (16, 15), (17, 13), (17, 16)]
        self.assertEqual(co, exp_co)


if __name__ == "__main__":
    unittest.main()
