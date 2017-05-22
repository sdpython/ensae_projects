#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest


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
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from src.ensae_projects.datainc.croix_rouge import encrypt_file, decrypt_dataframe


class TestNotebookHackathonEncrypt(unittest.TestCase):

    def test_encrypt(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        pwd = (b"example" * 3)[:16]
        temp = get_temp_folder(__file__, "temp_encrypt")
        infile = os.path.join(temp, "..", "data", "ITMMASTER.schema.txt")
        outfile = os.path.join(temp, "ITMMASTER.schema.enc")
        encrypt_file(infile, outfile, password=pwd)
        assert os.path.exists(outfile)

        df = decrypt_dataframe(outfile, password=pwd)
        fLOG(df.shape)
        fLOG(df)
        assert len(df) > 0

        if not is_travis_or_appveyor():
            for infile in ["meaning_invoice.txt", "SINVOICE.schema.txt", "SINVOICEV.schema.txt", "stojou.schema.txt"]:
                if os.path.exists(infile):
                    encrypt_file(infile, infile.replace(".txt", ".enc"))


if __name__ == "__main__":
    unittest.main()
