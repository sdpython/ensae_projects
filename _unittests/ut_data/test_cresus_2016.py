#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings
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


try:
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyensae as skip__


from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from pyquickhelper.filehelper.encryption import decrypt_stream
from src.ensae_projects.data.data_cresus import process_cresus_whole_process, cresus_dummy_file
from pyquickhelper.filehelper.compression_helper import unzip_files


class TestCresus2016(unittest.TestCase):

    def test_process_data(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if is_travis_or_appveyor():
            warnings.warn("disabled on appveyor and travis")
            return
        temp = get_temp_folder(__file__, "temp_process_data_cresus_2016")
        import keyring
        pwd = keyring.get_password(
            "cresus", os.environ["COMPUTERNAME"] + "ensae")
        assert pwd
        name = cresus_dummy_file()
        if not os.path.exists(name):
            raise FileNotFoundError(name)
        zipname = os.path.join(temp, "bdd.zip")
        pwd = pwd.encode("ascii")
        decrypt_stream(pwd, name, zipname)
        res = unzip_files(zipname, temp)
        fLOG(res)
        infile = res[0]
        train, test = process_cresus_whole_process(
            infile, outfold=temp, fLOG=fLOG)
        for r in train.values():
            df = pandas.read_csv(r, sep="\t", encoding="utf-8")
            fLOG(df.columns)


if __name__ == "__main__":
    unittest.main()
