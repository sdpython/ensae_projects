#-*- coding: utf-8 -*-
"""
@brief      test log(time=60s)
"""

import sys
import os
import unittest
import warnings


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
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from src.ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook, unittest_raise_exception_notebook


class TestNotebookHackathon(unittest.TestCase):

    def test_notebook_hackathon(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor() == "appveyor":
            return
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_hackathon_2015")
        keepnote = ls_notebooks("hackathon_2015")
        assert len(keepnote) > 0
        keepnote = [
            _ for _ in keepnote if "database_schemas" not in _ and
            "process_clean_files" not in _ and
            "times_series" not in _ and
            "upload" not in _]

        def valid_cell(cell):
            if "%blob" in cell:
                return False
            if "blob_service" in cell:
                return False
            return True

        if len(keepnote) > 0:
            for _ in keepnote:
                fLOG(_)
            res = execute_notebooks(temp, keepnote, filter=lambda i, n: True, valid_cell=valid_cell,
                                    fLOG=fLOG, clean_function=clean_function_notebook)
            unittest_raise_exception_notebook(res, fLOG)
        else:
            warnings.warn("No notebook was tested for the hackathon 2015")


if __name__ == "__main__":
    unittest.main()
