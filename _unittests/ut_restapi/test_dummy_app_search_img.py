#-*- coding: utf-8 -*-
"""
@brief      test log(time=30s)
"""

import sys
import os
import unittest
import ujson
import falcon
import falcon.testing as testing


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

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, add_missing_development_version


class TestDummyAppSearchImg(testing.TestBase):

    def setUp(self):
        add_missing_development_version(["pymyinstall", "pyensae", "jyquickhelper",
                                         "pandas_streaming", "mlinsights", "lightmlrestapi"],
                                        __file__, hide=True)
        super().setUp()

    def before(self):
        from src.ensae_projects.restapi import search_images_dogcat
        temp = get_temp_folder(__file__, 'temp_search_images_dogcat')
        search_images_dogcat(self.api, dest=temp)

    def test_dummy_search_app_search_img(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from lightmlrestapi.args import image2base64

        # With a different image than the original.
        img2 = os.path.join(os.path.dirname(__file__),
                            "data", "wiki_modified.png")
        b64 = image2base64(img2)[1]
        bodyin = ujson.dumps({'X': b64})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        if self.srmock.status != falcon.HTTP_201:
            res = ujson.loads(body)
            raise Exception("Failure\n{0}".format(res['description']))
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 5)
        self.assertIsInstance(d['Y'][0][0][0], float)
        self.assertIsInstance(d['Y'][0][0][1], int)
        self.assertEqual(d['Y'][0][0][2].replace('\\', '/'), {
                         'name': 'oneclass/cat-2922832__480.jpg'})

    def test_dummy_error_img(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__ma²in__")

        from lightmlrestapi.args import image2base64, image2array, base642image

        img2 = os.path.join(os.path.dirname(__file__),
                            "data", "wiki_modified.png")
        ext_b64 = image2base64(img2)
        img2 = base642image(ext_b64[1]).convert('RGB')
        arr = image2array(img2)
        bodyin = ujson.dumps({'X': arr.tolist()})

        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        d = ujson.loads(body)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn("object has no attribute", d['description'])


if __name__ == "__main__":
    unittest.main()
