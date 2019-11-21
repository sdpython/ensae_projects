# -*- coding: utf-8 -*-
"""
@brief      test log(time=50s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from pyensae.datasource import download_data
from ensae_projects.datainc import convert_dcm2png


class TestLONGdcm(ExtTestCase):

    @classmethod
    def setUpClass(cls):
        temp = get_temp_folder(__file__, "temp_data_dcm")
        download_data("CBIS-DDSM.zip", whereTo=temp)
        cls.images = os.path.join(temp, "CBIS-DDSM")

    def test_convert_dcm2png(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_convert_dcm2png")
        df = convert_dcm2png(TestLONGdcm.images, temp, fLOG=fLOG)
        self.assertEqual(df.shape[0], 6)


if __name__ == "__main__":
    unittest.main()
