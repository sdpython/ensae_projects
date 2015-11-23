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
from src.ensae_projects.data.croix_rouge import get_meaning, merge_schema, df2rsthtml
from src.ensae_projects.data import PasswordException


class TestNotebookHackathon(unittest.TestCase):

    def test_meaning_table(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        try:
            df = get_meaning("invoice")
        except PasswordException:
            # the password is not available on this machine, set PWDCROIXROUGE
            return
        assert len(df) > 0

    def test_joined_schemas(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        temp = get_temp_folder(__file__, "temp_joined_schemas")

        try:
            df = merge_schema()
        except PasswordException:
            # the password is not available on this machine, set PWDCROIXROUGE
            return
        assert len(df) > 0
        outexc = os.path.join(temp, "schemas.xlsx")
        df.to_excel(outexc, index=False)
        fLOG(df.columns)
        txt = df2rsthtml(df, format="rst")
        assert "nan\t" not in txt
        fLOG("\n" + txt)

        outfile = os.path.join(temp, "schemas.rst")
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(txt)


if __name__ == "__main__":
    unittest.main()
