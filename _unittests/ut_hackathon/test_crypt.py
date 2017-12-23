"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import json
import pandas


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

from pyquickhelper.loghelper import fLOG
from src.ensae_projects.hackathon import enumerate_json_items
from src.ensae_projects.hackathon.crypt_helper import set_password, get_password


class TestCrypt(unittest.TestCase):

    def test_json_iter(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        set_password('ppwwdd', 'ep_ex')
        pwd = get_password('ep_ex')
        self.assertEqual('ppwwdd', pwd)


if __name__ == "__main__":
    unittest.main()
