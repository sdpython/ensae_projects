#-*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
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


try:
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyensae as skip__


from pyquickhelper.loghelper import fLOG
from src.ensae_projects.datainc.data_geo_streets import get_seattle_streets, shapely_records
from src.ensae_projects.datainc.data_geo_streets import seattle_streets_set_level2
from src.ensae_projects.challenge.city_tour import best_euler_path


class TestLONGCityTour(unittest.TestCase):

    def test_best_euler_path_level2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        name = get_seattle_streets()
        shapes, records, fields = shapely_records(name)
        edges_index, edges, vertices, distances = seattle_streets_set_level2(
            shapes, records)
        co, ind, d = best_euler_path(edges_index=edges_index, edges=edges,
                                     distances=distances, vertices=vertices, fLOG=fLOG)
        self.assertEqual(len(co), len(ind))
        assert d > 0


if __name__ == "__main__":
    unittest.main()
