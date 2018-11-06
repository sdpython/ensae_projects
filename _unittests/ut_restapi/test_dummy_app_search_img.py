# -*- coding: utf-8 -*-
"""
@brief      test log(time=30s)
"""

import sys
import os
import unittest
import warnings
from io import StringIO
from contextlib import redirect_stderr
import falcon
import falcon.testing as testing
import x86cpu
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, add_missing_development_version
from pyquickhelper.pycode import skipif_travis
import ujson

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


class TestDummyAppSearchImg(testing.TestCase):

    def setUp(self):
        add_missing_development_version(["pymyinstall", "pyensae", "jyquickhelper",
                                         "pandas_streaming", "mlinsights", "lightmlrestapi"],
                                        __file__, hide=True)
        super().setUp()

        from src.ensae_projects.restapi import search_images_dogcat
        temp = get_temp_folder(__file__, 'temp_search_images_dogcat')

        with redirect_stderr(StringIO()):
            try:
                from keras.applications.mobilenet import MobileNet
                assert MobileNet is not None
                self._run_test = True
            except SyntaxError as e:
                warnings.warn(
                    "tensorflow is probably not available yet on python 3.7: {0}".format(e))
                self._run_test = False
                return

        search_images_dogcat(self.api, dest=temp)

    @skipif_travis('tensorflow/python/lib/core/bfloat16.cc:664] Check failed: PyBfloat16_Type.tp_base != nullptr')
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

        if not self._run_test:
            return

        result = self.simulate_request(path='/', method="POST", body=bodyin)
        if result.status != falcon.HTTP_201:
            raise Exception("Failure\n{0}".format(result.status))
        self.assertEqual(result.status, falcon.HTTP_201)
        d = ujson.loads(result.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 5)
        self.assertIsInstance(d['Y'][0][0], float)
        self.assertIsInstance(d['Y'][0][1], int)
        self.assertIn('name', d['Y'][0][2])
        val = d['Y'][0][2]['name'].replace('\\', '/')
        self.assertIn(val, ('oneclass/cat-2922832__480.jpg',
                            'oneclass/wolf-2865653__480.jpg'))

    @skipif_travis('tensorflow/python/lib/core/bfloat16.cc:664] Check failed: PyBfloat16_Type.tp_base != nullptr')
    @unittest.skipIf(not x86cpu.info.supports_avx2, "tensorflow requires instructions AVX2 on CPU")
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

        if not self._run_test:
            return

        result = self.simulate_request(path='/', method="POST", body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_400)
        d = ujson.loads(result.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn("object has no attribute", d['description'])


if __name__ == "__main__":
    unittest.main()
