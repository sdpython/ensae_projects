# -*- coding: utf-8 -*-
"""
@brief      test log(time=60s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from pyquickhelper.ipythonhelper import execute_notebook_list_finalize_ut
from ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook
import ensae_projects


class TestNotebookHackathon(unittest.TestCase):

    def test_notebook_hackathon(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor():
            return
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_hackathon_2015")
        keepnote = ls_notebooks("hackathon_2015")
        self.assertTrue(len(keepnote) > 0)
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

        res = execute_notebooks(temp, keepnote, filter=lambda i, n: True, valid_cell=valid_cell,
                                fLOG=fLOG, clean_function=clean_function_notebook)
        execute_notebook_list_finalize_ut(
            res, fLOG=fLOG, dump=ensae_projects)


if __name__ == "__main__":
    unittest.main()
