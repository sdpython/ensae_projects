# -*- coding: utf-8 -*-
"""
@brief      test log(time=50s)
"""

import sys
import os
import unittest
import random
from datetime import time
import pandas
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from ensae_projects.datainc.data_bikes import (
    get_chicago_stations, folium_html_stations_map, add_missing_time)


class TestStationsChicago(ExtTestCase):

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
        ExtTestCase.setUpClass()

    def test_folium_html_station_map(self):
        df_stations = self._stations
        colors = ["red", "blue"]
        draw = []
        for iter in df_stations.apply(lambda row: (row["latitude"], row["longitude"]), axis=1):  # pylint: disable=W0622
            x, y = iter
            h = random.randint(0, 1)
            draw.append(((x, y), colors[h]))
            if len(draw) > 10:
                break
        map_osm = folium_html_stations_map(draw)
        assert map_osm

    def test_add_missing_time(self):
        df = pandas.DataFrame(dict(A=["un", "deux"], B=[1, 2],
                                   C=[time(12, 0, 0), time(12, 10, 0)]))
        fLOG(df)
        dfj = add_missing_time(df, "C", values="B")
        # fLOG(dfj[dfj.B != 0])
        self.assertEqual(dfj.shape, (2 * 24 * 6, 3))
        g = dfj.B.dropna()
        self.assertEqual(len(g), 2 * 24 * 6)


if __name__ == "__main__":
    unittest.main()
