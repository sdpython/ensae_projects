# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import (
    ExtTestCase, get_temp_folder, is_travis_or_appveyor)
from pyquickhelper.loghelper import get_password
from ensae_projects.datainc.croix_rouge import get_meaning, merge_schema, df2rsthtml
from ensae_projects.datainc import PasswordException


class TestNotebookHackathon(ExtTestCase):

    def test_meaning_table(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor():
            warnings.warn("disabled on appveyor")
            return
        try:
            df = get_meaning("invoice")
        except PasswordException:
            # the password is not available on this machine
            return
        assert len(df) > 0

    def test_joined_schemas(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor():
            warnings.warn("disabled")
            return
        temp = get_temp_folder(__file__, "temp_joined_schemas")
        try:
            df = merge_schema()
        except PasswordException:
            # the password is not available on this machine
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
