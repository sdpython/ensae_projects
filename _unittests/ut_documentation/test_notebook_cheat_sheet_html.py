# -*- coding: utf-8 -*-
"""
@brief      test log(time=32s)
"""

import sys
import os
import unittest
import shutil
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv
from pyquickhelper.ipythonhelper import execute_notebook_list_finalize_ut
from ensae_projects.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook
import ensae_projects


class TestNotebookCheatSheetHtml(unittest.TestCase):

    def test_notebook_cheatsheet_html(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor() == "appveyor":
            # connectivity issue
            return

        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_cheat_sheet_html")
        keepnote = ls_notebooks("cheat_sheets")
        self.assertTrue(len(keepnote) > 0)
        keepnote = [_ for _ in keepnote if "chsh_files" not in _]

        if len(keepnote) > 0:
            fold = os.path.dirname(keepnote[0])
            copy = [os.path.join(fold, "geo_data.zip")]
            for c in copy:
                shutil.copy(c, temp)

        res = execute_notebooks(temp, keepnote,
                                lambda i, n: "deviner" not in n and "html" in n,
                                fLOG=fLOG,
                                clean_function=clean_function_notebook)
        execute_notebook_list_finalize_ut(
            res, fLOG=fLOG, dump=ensae_projects)


if __name__ == "__main__":
    unittest.main()
