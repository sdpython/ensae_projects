# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import pandas
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from ensae_projects.datainc import enumerate_text_lines, change_encoding_improve, clean_column_name_sql_dump


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
        ls = list(enumerate_text_lines(filename, encoding="utf-8",
                                       quotes_as_str=True, clean_column_name=clean_column_name))
        fLOG(ls)
        assert len(ls) == 1

    def test_clean_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        filename = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "data", "wrong_columns.txt")
        temp = get_temp_folder(__file__, "temp_clean_file")

        def clean_column_name(i, line, hist):
            a, b = clean_column_name_sql_dump(i, line, hist)
            return a.replace("_0", ""), b

        out = os.path.join(temp, "clean.txt")
        change_encoding_improve(filename, out, "ascii",
                                "ascii", clean_column_name)

        df = pandas.read_csv(out, sep=";")
        fLOG(df.shape)
        fLOG(df)
        self.assertEqual(df.iloc[2, 1], "5;6")
        self.assertEqual(df.iloc[2, 2], 7)


if __name__ == "__main__":
    unittest.main()
