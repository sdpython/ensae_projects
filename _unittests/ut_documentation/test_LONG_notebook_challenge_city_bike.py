#-*- coding: utf-8 -*-
"""
@brief      test log(time=1000s)
"""

import sys
import os
import unittest
import shutil


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
    import jyquickhelper as skip___
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "jyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import jyquickhelper as skip___

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
from src.ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook, unittest_raise_exception_notebook


class TestLONGNotebookChallengeCityBike(unittest.TestCase):

    def test_long_notebook_challenge_city_tour(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_long_challenge_city_bike")
        keepnote = ls_notebooks(os.path.join("challenges", "city_bike"))
        assert len(keepnote) > 0
        folder = os.path.dirname(keepnote[0])
        images = [os.path.join(folder, "images", "chicago.png")]
        dest = os.path.join(temp, "images")
        if not os.path.exists(dest):
            os.mkdir(dest)
        for img in images:
            shutil.copy(img, dest)
        if len(keepnote) > 0:
            res = execute_notebooks(temp, keepnote,
                                    lambda i, n: "bike" in n,
                                    fLOG=fLOG,
                                    clean_function=clean_function_notebook)
            unittest_raise_exception_notebook(res, fLOG)
        else:
            raise Exception("no notebook")


if __name__ == "__main__":
    unittest.main()