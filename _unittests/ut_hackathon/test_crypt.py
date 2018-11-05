"""
@brief      test log(time=8s)
"""

import sys
import os
import warnings
import unittest
from pyquickhelper.pycode import skipif_travis


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


from src.ensae_projects.hackathon.crypt_helper import set_password, get_password


class TestCrypt(unittest.TestCase):

    def test_json_iter(self):
        try:
            set_password('ppwwdd', 'ep_ex')
        except RuntimeError as e:
            if "keyrings.alt" in str(e):
                warnings.warn("No recommended backend was available.")
                return
            else:
                raise e
        pwd = get_password('ep_ex')
        self.assertEqual('ppwwdd', pwd)


if __name__ == "__main__":
    unittest.main()
