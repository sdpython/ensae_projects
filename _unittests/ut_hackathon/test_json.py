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
from src.ensae_projects.hackathon.json_helper import extract_images_from_json_2017


class TestJson(unittest.TestCase):

    def test_json_iter(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "example_json.json")
        records = list(enumerate_json_items(data))
        self.assertEqual(len(records), 2)
        js = json.dumps(records)
        records = list(enumerate_json_items(js))
        js2 = json.dumps(records)
        self.assertEqual(js, js2)

    def test_product_sample(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "product_sample.json")
        imgs = list(extract_images_from_json_2017(data))
        self.assertEqual(len(imgs), 1)
        self.assertEqual(imgs[0]['image_path'], 'https://coucou.JPEG')
        df = pandas.DataFrame(imgs)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.shape[1], 26)


if __name__ == "__main__":
    unittest.main()
