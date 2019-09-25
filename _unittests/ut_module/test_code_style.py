"""
@brief      test log(time=1000s)
"""

import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


def _run_cmd_filter(name):
    return "data_bikes.py" not in name


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_style_src(self):
        """Checks style of source files."""
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG, verbose=False, run_cmd_filter=_run_cmd_filter,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0212', 'W0107', 'C0415'),
                   skip=["Use % formatting in logging functions and pass the % parameters",
                         "Redefining built-in 'next'",
                         "Redefining name 'fLOG' from outer scope ",
                         "Redefining built-in 'format'",
                         "Redefining built-in 'iter' ",
                         "Redefining built-in 'filter'",
                         "json_helper.py:131: E1137",
                         "json_helper.py:149: E1137",
                         "json_helper.py:155: E1137",
                         "image_helper.py:11: R1710",
                         "city_tour.py:428: R1710",
                         "croix_rouge.py:150: E0602",
                         "blossom.py:690: W0612",
                         "blossom.py:693: W0612",
                         "Instance of 'X86Info' has no 'supports_avx2'",
                         "data_bikes.py:1: F0002",
                         'maximum recursion depth exceeded',
                         "R1720",
                         ])

    def test_style_test(self):
        """Checks style of tests files."""
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*", verbose=False,
                   run_cmd_filter=_run_cmd_filter,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'C0414', 'W0107', 'W0611', 'C0415'),
                   skip=["Module 'ujson' has no 'loads'",
                         "Redefining built-in 'iter'",
                         "Redefining name 'path' from outer scope",
                         "Module 'ujson' has no 'dumps'",
                         "Instance of 'X86Info' has no 'supports_avx2'",
                         "maximum recursion depth exceeded",
                         "R1720",
                         "Module 'falcon' has no 'HTTP_",
                         ])


if __name__ == "__main__":
    unittest.main()
