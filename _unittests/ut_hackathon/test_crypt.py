"""
@brief      test log(time=8s)
"""

import sys
import os
import warnings
import unittest
from ensae_projects.hackathon.crypt_helper import set_password, get_password


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
