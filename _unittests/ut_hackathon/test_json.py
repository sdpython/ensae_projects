"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import json
import pandas
from ensae_projects.hackathon import enumerate_json_items
from ensae_projects.hackathon.json_helper import extract_images_from_json_2017


class TestJson(unittest.TestCase):

    def test_json_iter(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "example_json.json")
        records = list(enumerate_json_items(data))
        self.assertEqual(len(records), 2)
        js = json.dumps(records)
        records = list(enumerate_json_items(js))
        js2 = json.dumps(records)
        self.assertEqual(js, js2)

    def test_product_sample(self):
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
