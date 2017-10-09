#-*- coding: utf-8 -*-
"""
@brief      test log(time=50s)
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
from pyquickhelper.pycode import get_temp_folder
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from src.ensae_projects.datainc.data_geo_streets import get_seattle_streets, shapely_records, folium_html_street_map, get_fields_description
from src.ensae_projects.datainc.data_geo_streets import build_streets_vertices, plot_streets_network
from src.ensae_projects.datainc.data_geo_streets import seattle_streets_set_level2, seattle_streets_set_small


class TestStreetsSeattle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fLOG("download and load the shapes")
        temp = get_temp_folder(__file__, "temp_seattle_shapes_records")
        name = get_seattle_streets(folder=temp)
        shapes, records, fields = shapely_records(name)
        cls._shapes = shapes
        cls._records = records
        cls._fields = fields

    def test_seattle_shapes_records(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        records = self._records
        fields = self._fields
        assert shapes
        assert records
        d = {k[0]: v for k, v in zip(fields[1:], records[0])}
        assert len(d) > 0

    def test_folium_html_street_map(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        subset = list(range(0, 10))
        map_osm = folium_html_street_map(subset, shapes)
        assert map_osm

    def test_folium_html_street_map_odd(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        subset = list(range(0, 10))
        map_osm = folium_html_street_map(subset, shapes, color_vertices="odd")
        assert map_osm

    def test_build_streets_vertices(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        subset = list(range(0, 10))
        vertices, edges = build_streets_vertices(subset, shapes)
        fLOG(vertices)
        fLOG(edges)
        self.assertEqual(len(edges), len(subset))
        if len(vertices) > len(edges) * 2:
            raise Exception("{0} > {1}\n{2}\n{3}".format(
                len(vertices), len(edges), edges, vertices))

    def test_plot_streets_network(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        fix_tkinter_issues_virtualenv()
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        subset = list(range(0, 10))
        vertices, edges = build_streets_vertices(subset, shapes)
        plot_streets_network(subset, edges, vertices, shapes, ax=ax)
        temp = get_temp_folder(__file__, "temp_plot_streets_network")
        img = os.path.join(temp, "out_img.png")
        fig.savefig(img)
        plt.close('all')
        assert os.path.exists(img)

    def test_plot_streets_network_odd(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        fix_tkinter_issues_virtualenv()
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        subset = list(range(0, 10))
        vertices, edges = build_streets_vertices(subset, shapes)
        plot_streets_network(subset, edges, vertices,
                             shapes, ax=ax, color_vertices='odd')
        temp = get_temp_folder(__file__, "temp_plot_streets_network_odd")
        img = os.path.join(temp, "out_img.png")
        fig.savefig(img)
        plt.close('all')
        assert os.path.exists(img)

    def test_seattle_description(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = get_fields_description()
        assert df.shape[0] > 0
        assert df.shape[1] > 0

    def test_seattle_streets_set_small(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        edges_index, edges, vertices, distances = seattle_streets_set_small(
            self._shapes, self._records)
        assert vertices
        assert edges
        assert edges_index
        assert distances
        self.assertEqual(len(edges_index), len(edges))
        self.assertEqual(len(edges_index), len(distances))

    def test_seattle_streets_set_level2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        shapes = self._shapes
        records = self._records
        edges_index, edges, vertices, distances = seattle_streets_set_level2(
            shapes, records)
        assert vertices
        assert edges
        assert edges_index
        assert distances
        self.assertEqual(len(edges_index), len(edges))
        self.assertEqual(len(edges_index), len(distances))


if __name__ == "__main__":
    unittest.main()
