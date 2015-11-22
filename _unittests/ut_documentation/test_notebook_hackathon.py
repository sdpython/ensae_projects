#-*- coding: utf-8 -*-
"""
@brief      test log(time=60s)
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
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from src.ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook, unittest_raise_exception_notebook


class TestNotebookHackathon(unittest.TestCase):

    def test_notebook_hackathon(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_hackathon_2015")
        keepnote = ls_notebooks("hackathon_2015")
        assert len(keepnote) > 0
        keepnote = [
            _ for _ in keepnote if "upload" not in _ and "exploration" not in _]
        if len(keepnote) > 0:
            res = execute_notebooks(temp, keepnote,
                                    lambda i, n: "deviner" not in n,
                                    fLOG=fLOG,
                                    clean_function=clean_function_notebook)
            unittest_raise_exception_notebook(res, fLOG)

if __name__ == "__main__":
    unittest.main()
