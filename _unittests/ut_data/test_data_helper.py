#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import re

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
from src.ensae_projects.data import enumerate_text_lines


class TestNotebookHackathon(unittest.TestCase):

    def test_meaning_table(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "data_qutoes.txt")
        def clean_column_name(s):
            return s.replace("_0", "")
        l = list(enumerate_text_lines(filename, encoding="utf-8", quotes_as_str=True, clean_column_name=clean_column_name))
        fLOG(l)
        assert len(l) == 1


if __name__ == "__main__":
    unittest.main()
