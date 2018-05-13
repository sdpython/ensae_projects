# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor

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

from src.ensae_projects.automation import get_password, set_password


class TestKeyring(unittest.TestCase):

    def test_keyring(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            warnings.warn("keyring on tested on travis and appveyor")
            return
        set_password("k1", "k2", "kk")
        v = get_password("k1", "k2")
        self.assertEqual(v, "kk")


if __name__ == "__main__":
    unittest.main()
