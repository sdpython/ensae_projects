"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
from PIL import Image
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, ExtTestCase


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

from src.ensae_projects.hackathon.image_helper import resize_image


class TestImage(ExtTestCase):

    def test_image(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "white.png")
        temp = get_temp_folder(__file__, "temp_resize_mage")

        dest = os.path.join(temp, "mini.png")
        resize_image(data, dest=dest, maxdim=200)
        self.assertExists(dest)
        im = Image.open(dest)
        self.assertGreater(200, min(im.size))

        dest = os.path.join(temp, "mini2.png")
        resize_image(data, dest=dest, maxdim=100)
        self.assertExists(dest)
        im = Image.open(dest)
        self.assertGreater(100, min(im.size))


if __name__ == "__main__":
    unittest.main()
