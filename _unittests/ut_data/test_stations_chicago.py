#-*- coding: utf-8 -*-
"""
@brief      test log(time=50s)
"""

import sys
import os
import unittest
import random
from datetime import time
import pandas


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
from src.ensae_projects.data.data_bikes import get_chicago_stations, folium_html_stations_map, add_missing_time


class TestStationsChicago(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fLOG("download and load the shapes")
        temp = get_temp_folder(__file__, "temp_stations_chicago")
        df_stations, df_trips = get_chicago_stations(folder=temp, as_df=True)
        if len(df_stations) == 0:
            raise Exception("empty dataframe")
        if len(df_trips) == 0:
            raise Exception("empty dataframe")
        cls._stations = df_stations
        cls._trips = df_trips

    def test_folium_html_station_map(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df_stations = self._stations
        colors = ["red", "blue"]
        draw = []
        for iter in df_stations.apply(lambda row: (row["latitude"], row["longitude"]), axis=1):
            x, y = iter
            h = random.randint(0, 1)
            draw.append(((x, y), colors[h]))
            if len(draw) > 10:
                break
        map_osm = folium_html_stations_map(draw)
        assert map_osm

    def test_add_missing_time(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        df = pandas.DataFrame(dict(A=["un", "deux"], B=[1, 2], C=[
                              time(12, 0, 0), time(12, 10, 0)]))
        fLOG(df)
        dfj = add_missing_time(df, "C")
        # fLOG(dfj[dfj.B != 0])
        self.assertEqual(dfj.shape, (24 * 60 // 10, 3))
        g = dfj.B.dropna()
        self.assertEqual(len(g), 24 * 60 // 10)
        g = dfj.A.dropna()
        self.assertEqual(len(g), 2)


if __name__ == "__main__":
    unittest.main()
