# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings
import pandas
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import (
    ExtTestCase, get_temp_folder, is_travis_or_appveyor)
from pyquickhelper.filehelper.encryption import decrypt_stream
from pyquickhelper.filehelper.compression_helper import unzip_files
from pyquickhelper.loghelper import get_password
from ensae_projects.datainc.data_cresus import (
    process_cresus_whole_process, cresus_dummy_file)


class TestCresus2016(ExtTestCase):

    def test_process_data(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor():
            warnings.warn("disabled on appveyor and travis")
            return
        temp = get_temp_folder(__file__, "temp_process_data_cresus_2016")
        pwd = get_password("cresus", "ensae_projects,ensae", ask=False)
        self.assertNotEmpty(pwd)
        name = cresus_dummy_file()
        self.assertExists(name)
        zipname = os.path.join(temp, "bdd.zip")
        pwd = pwd.encode("ascii")
        decrypt_stream(pwd, name, zipname)
        res = unzip_files(zipname, temp)
        fLOG(res)
        infile = res[0]
        train, _ = process_cresus_whole_process(
            infile, outfold=temp, fLOG=fLOG)
        for r in train.values():
            df = pandas.read_csv(r, sep="\t", encoding="utf-8")
            fLOG(df.columns)


if __name__ == "__main__":
    unittest.main()
