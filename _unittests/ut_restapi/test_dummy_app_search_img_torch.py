# -*- coding: utf-8 -*-
"""
@brief      test log(time=13s)
"""

import sys
import os
import unittest
import warnings
from io import StringIO
from contextlib import redirect_stderr
import falcon
import falcon.testing as testing
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, add_missing_development_version
from pyquickhelper.pycode import skipif_travis
import ujson


def has_torch():
    try:
        import torch
        return torch is not None
    except ImportError:
        return False


class TestDummyAppSearchImgTorch(testing.TestCase):

    def setUp(self):
        super(TestDummyAppSearchImgTorch, self).setUp()
        add_missing_development_version(["pymyinstall", "pyensae", "jyquickhelper",
                                         "pandas_streaming", "mlinsights", "lightmlrestapi"],
                                        __file__, hide=True)
        super().setUp()

        from ensae_projects.restapi import search_images_dogcat
        temp = get_temp_folder(__file__, 'temp_search_images_dogcat_torch')

        with redirect_stderr(StringIO()):
            try:
                from torchvision.models import squeezenet1_1  # pylint: disable=E0401
                assert squeezenet1_1 is not None
                self._run_test = True
            except SyntaxError as e:
                warnings.warn(
                    "torch is not available: {0}".format(e))
                self._run_test = False
                return

        self.app = search_images_dogcat(self.app, dest=temp, module="torch")

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
        bodyin = ujson.dumps({'X': b64})  # pylint: disable=E1101

        if not self._run_test:
            return

        result = self.simulate_request(path='/', method="POST", body=bodyin)
        if result.status != falcon.HTTP_201:  # pylint: disable=E1101
            raise Exception("Failure\n{0}".format(result.status))
        self.assertEqual(
            result.status, falcon.HTTP_201)  # pylint: disable=E1101
        d = ujson.loads(result.content)  # pylint: disable=E1101
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 5)
        self.assertIsInstance(d['Y'][0][0], float)
        self.assertIsInstance(d['Y'][0][1], int)
        self.assertIn('name', d['Y'][0][2])
        val = d['Y'][0][2]['name'].replace('\\', '/')
        val = "/".join(val.split("/")[-2:])
        self.assertIn(val, ('oneclass/cat-188088__480.jpg',
                            'oneclass/shotlanskogo-2934720__480.jpg',
                            'oneclass/dog-2684073__480.jpg',
                            'oneclass/fun-2213606__480.jpg',
                            'oneclass/dog-2863719__480.jpg',
                            'oneclass/wolf-2865653__480.jpg',
                            'oneclass/dog-2687502__480.jpg'))

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
        bodyin = ujson.dumps({'X': arr.tolist()})  # pylint: disable=E1101

        if not self._run_test:
            return

        result = self.simulate_request(path='/', method="POST", body=bodyin)
        self.assertEqual(
            result.status, falcon.HTTP_400)  # pylint: disable=E1101
        d = ujson.loads(result.content)  # pylint: disable=E1101
        self.assertIn('Unable to predict', d['title'])
        self.assertIn("object has no attribute", d['description'])


if __name__ == "__main__":
    unittest.main()
