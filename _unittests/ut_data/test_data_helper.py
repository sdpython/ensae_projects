#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import re
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
    import pyquickhelper
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
    import pyquickhelper

try:
    import pyensae
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
    import pyensae

from pyquickhelper import fLOG, get_temp_folder
from src.ensae_projects.data import enumerate_text_lines, change_encoding_improve, clean_column_name_sql_dump


class TestNotebookHackathon(unittest.TestCase):

    def test_meaning_table(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        filename = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "data", "data_qutoes.txt")

        def clean_column_name(s):
            return s.replace("_0", "")
        l = list(enumerate_text_lines(filename, encoding="utf-8",
                                      quotes_as_str=True, clean_column_name=clean_column_name))
        fLOG(l)
        assert len(l) == 1

    def test_clean_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        filename = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "data", "wrong_columns.txt")
        temp = get_temp_folder(__file__, "temp_clean_file")

        reg = re.compile(';"(.*?)"')

        def clean_column_name(i, line, hist):
            a, b = clean_column_name_sql_dump(i, line, hist)
            return a.replace("_0", ""), b

        out = os.path.join(temp, "clean.txt")
        change_encoding_improve(filename, out, "ascii",
                                "ascii", clean_column_name)

        df = pandas.read_csv(out, sep=";")
        fLOG(df.shape)
        fLOG(df)
        self.assertEqual(df.ix[2, 1], "5;6")
        self.assertEqual(df.ix[2, 2], 7)


if __name__ == "__main__":
    unittest.main()
