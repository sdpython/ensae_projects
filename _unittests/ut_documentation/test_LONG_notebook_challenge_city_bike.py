# -*- coding: utf-8 -*-
"""
@brief      test log(time=1000s)
"""

import sys
import os
import unittest
import shutil
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from pyquickhelper.ipythonhelper import execute_notebook_list_finalize_ut


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


from src.ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook
import src.ensae_projects


class TestLONGNotebookChallengeCityBike(unittest.TestCase):

    def test_long_notebook_challenge_city_tour(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_long_challenge_city_bike")
        keepnote = ls_notebooks(os.path.join("challenges", "city_bike"))
        self.assertTrue(len(keepnote) > 0)
        folder = os.path.dirname(keepnote[0])
        images = [os.path.join(folder, "images", "chicago.png")]
        dest = os.path.join(temp, "images")
        if not os.path.exists(dest):
            os.mkdir(dest)
        for img in images:
            shutil.copy(img, dest)
        res = execute_notebooks(temp, keepnote,
                                lambda i, n: "bike" in n,
                                fLOG=fLOG,
                                clean_function=clean_function_notebook)
        execute_notebook_list_finalize_ut(
            res, fLOG=fLOG, dump=src.ensae_projects)


if __name__ == "__main__":
    unittest.main()
