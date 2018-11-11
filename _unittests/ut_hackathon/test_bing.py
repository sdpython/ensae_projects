"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
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

from src.ensae_projects.hackathon.web_search_helper import query_bing_image, extract_bing_result


def _has_selenium():
    try:
        import selenium
        return selenium is not None
    except ImportError:
        return False


class TestBing(ExtTestCase):

    def test_web_search_helper(self):
        temp = get_temp_folder(__file__, "temp_web_search_helper2")
        res = query_bing_image("inondations france", folder_cache=temp)
        res = list(sorted(res))
        self.assertNotEmpty(res)
        self.assertEqual(
            res[0], "http://dailynous.com/wp-content/uploads/2017/08/hurricane-harvey-3.jpg")

    @unittest.skipIf(not _has_selenium(), reason="selenium not installed")
    def _test_web_search_helper_selenium(self):
        temp = get_temp_folder(__file__, "temp_web_search_helper_selenium")
        res = query_bing_image("inondations france",
                               folder_cache=temp, use_selenium=True)
        res = list(sorted(res))
        self.assertNotEmpty(res)
        self.assertEqual(
            res[0], "http://dailynous.com/wp-content/uploads/2017/08/hurricane-harvey-3.jpg")

    def test_extract_images(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, 'data', 'inon.html')
        with open(data, 'r', encoding='utf-8') as f:
            content = f.read()
        res = list(sorted(extract_bing_result(content)))
        self.assertNotEmpty(res)
        self.assertEqual(
            res[0], "http://s2.lemde.fr/image/2016/06/02/0x0/4931734_6_4ece_paris-le-2-juin_150113fa73261e9f5df771624f4aeb0f.jpg")

    def test_extract_images_file(self):
        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, 'data', 'inon.html')
        res = list(sorted(extract_bing_result(data)))
        self.assertNotEmpty(res)
        self.assertEqual(
            res[0], "http://s2.lemde.fr/image/2016/06/02/0x0/4931734_6_4ece_paris-le-2-juin_150113fa73261e9f5df771624f4aeb0f.jpg")


if __name__ == "__main__":
    unittest.main()
