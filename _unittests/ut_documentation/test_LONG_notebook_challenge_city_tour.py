# -*- coding: utf-8 -*-
"""
@brief      test log(time=160s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from pyquickhelper.ipythonhelper import execute_notebook_list_finalize_ut
from ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook
import ensae_projects


class TestLONGNotebookChallengeCityTour(unittest.TestCase):

    def test_long_notebook_challenge_city_tour(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_challenge_city_tour")
        keepnote = ls_notebooks(os.path.join("challenges", "city_tour"))
        self.assertTrue(len(keepnote) > 0)
        keepnote = [_ for _ in keepnote]
        res = execute_notebooks(temp, keepnote,
                                lambda i, n: "tour" in n,
                                fLOG=fLOG,
                                clean_function=clean_function_notebook)
        execute_notebook_list_finalize_ut(
            res, fLOG=fLOG, dump=ensae_projects)


if __name__ == "__main__":
    unittest.main()
