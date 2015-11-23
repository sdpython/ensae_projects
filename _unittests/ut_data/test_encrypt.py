#-*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import re

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
    import pyquickhelper
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
    import pyquickhelper

try:
    import pyensae
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
    import pyensae

from pyquickhelper import fLOG, get_temp_folder
from src.ensae_projects.data.croix_rouge import get_meaning, encrypt_file, decrypt_dataframe


class TestNotebookHackathonEncrypt(unittest.TestCase):

    def test_encrypt(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        pwd = ("example" * 3)[:16]
        temp = get_temp_folder(__file__, "temp_encrypt")
        infile = os.path.join(temp, "..", "data", "ITMMASTER.schema.txt")
        outfile = os.path.join(temp, "ITMMASTER.schema.enc")
        encrypt_file(infile, outfile, password=pwd)
        assert os.path.exists(outfile)

        df = decrypt_dataframe(outfile, password=pwd)
        fLOG(df.shape)
        fLOG(df)
        assert len(df) > 0

        if True:
            for infile in ["meaning_invoice.txt", "SINVOICE.schema.txt", "SINVOICEV.schema.txt", "stojou.schema.txt"]:
                if os.path.exists(infile):
                    encrypt_file(infile, infile.replace(".txt", ".enc"))


if __name__ == "__main__":
    unittest.main()