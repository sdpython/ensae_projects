# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
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


class TestNotebookCheatSheetFilesPip(unittest.TestCase):

    def test_notebook_cheatsheet_files_pip(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()
        temp = get_temp_folder(__file__, "temp_cheat_sheet_files_pip")
        keepnote = ls_notebooks("cheat_sheets")
        self.assertTrue(len(keepnote) > 0)
        keepnote = [_ for _ in keepnote if "chsh_files" not in _]

        if len(keepnote) > 0:
            fold = os.path.dirname(keepnote[0])
            copy = [os.path.join(fold, "geo_data.zip"),
                    os.path.join(fold, "images1.jpg")]
            for c in copy:
                shutil.copy(c, temp)
            copy = [os.path.join(fold, "tomates", "imgt_61.jpg"),
                    os.path.join(fold, "tomates", "imgt_66.jpg")]
            tempt = os.path.join(temp, "tomates")
            os.mkdir(tempt)
            for c in copy:
                shutil.copy(c, tempt)

        res = execute_notebooks(temp, keepnote,
                                lambda i, n: "pip" in n,
                                fLOG=fLOG,
                                clean_function=clean_function_notebook)
        execute_notebook_list_finalize_ut(
            res, fLOG=fLOG, dump=src.ensae_projects)


if __name__ == "__main__":
    unittest.main()
