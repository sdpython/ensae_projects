"""
@brief      test tree node (time=7s)
"""
import os
import unittest
from io import StringIO
from pyquickhelper.pycode import ExtTestCase
from pyquickhelper.loghelper import fLOG, BufferedPrint
from ensae_projects.__main__ import main


class TestCliImgHelper(ExtTestCase):

    def test_help(self):
        st = BufferedPrint()
        main(args=[], fLOG=st.fprint)
        res = str(st)
        self.assertIn("python -m ensae_projects <command>", res)
        self.assertIn("Converts all medical images", res)

    def test_dcm2img_help(self):
        st = BufferedPrint()
        main(args="dcm2png --help".split(), fLOG=st.fprint)
        res = str(st)
        self.assertIn("Converts all medical images", res)


if __name__ == "__main__":
    unittest.main()
