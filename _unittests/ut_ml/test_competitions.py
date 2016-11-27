"""
@brief      test log(time=8s)
"""

import sys
import os
import unittest
import shutil


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
from pyquickhelper.pycode import get_temp_folder
from src.ensae_projects.ml.competitions import AUC, AUC_multi, AUC_multi_multi
from src.ensae_projects.ml.competitions import private_codalab_wrapper_binary_classification, private_codalab_wrapper_multi_classification


class TestCompetitions(unittest.TestCase):

    def test_auc(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        ans = [1, 1, 1, 1, 1, 0, 0, 0, 0]
        score = [i * 0.8 + 0.1 for i in ans]
        a = AUC(ans, score)
        self.assertEqual(a, 1)
        score = [-i * 0.8 - 0.1 for i in ans]
        a = AUC(ans, score)
        self.assertEqual(a, 0)
        score = [i * 0.8 + 0.1 for i in ans]
        score[0] = 0.4
        score[-1] = 0.6
        a = AUC(ans, score)
        self.assertEqual(a, 0.95)

    def test_auc_multi(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = ["a", "b"]
        ans = [data[i] for i in [1, 1, 1, 1, 1, 0, 0, 0, 0]]
        score = [(i, data.index(i) * 0.8 + 0.1) for i in ans]
        a = AUC_multi(ans, score)
        self.assertEqual(a, 1)
        score = [("b", -data.index(i) * 0.8 - 0.1) for i in ans]
        a = AUC_multi(ans, score)
        self.assertEqual(a, 0)
        score = [("b", data.index(i) * 0.8 + 0.1) for i in ans]
        score[0] = (score[0][0], 0.4)
        score[-1] = (score[-1][0], 0.6)
        a = AUC_multi(ans, score)
        self.assertEqual(a, 0.95)

    def test_auc_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        ans = [1, 1, 1, 1, 1, 0, 0, 0, 0]
        score = [i * 0.8 + 0.1 for i in ans]
        score[0] = 0.4
        score[-1] = 0.6
        fLOG(score)
        t1 = get_temp_folder(__file__, "temp_answers")
        t2 = get_temp_folder(__file__, "temp_scores")
        f1 = "answer.txt"
        f2 = "answer.txt"
        fu1 = os.path.join(t1, f1)
        fu2 = os.path.join(t2, f2)
        out = os.path.join(t2, "scores.txt")
        with open(fu1, "w") as f:
            f.write("\n".join(str(_) for _ in ans))
        with open(fu2, "w") as f:
            f.write("\n".join(str(_) for _ in score))
        private_codalab_wrapper_binary_classification(
            AUC, "AUC", t1, t2, output=out)
        assert os.path.exists(out)
        with open(out, "r") as f:
            code = f.read()
        fLOG("**", code)

        self.assertEqual(code, "AUC:0.95")

    def test_auc_multi_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        t1 = get_temp_folder(__file__, "temp_multi_answers")
        t2 = get_temp_folder(__file__, "temp_multi_scores")
        t3 = get_temp_folder(__file__, "temp_multi_scores2")
        truth = os.path.join(
            t1, "..", "data", "tbl_test_dossier.Y.dummy.truth.txt")
        ans = os.path.join(t1, "..", "data", "tbl_test_dossier.Y.dummy.txt")
        f1 = "answer.txt"
        f2 = "answer.txt"
        shutil.copy(truth, os.path.join(t1, f1))
        shutil.copy(ans, os.path.join(t2, f2))

        with open(truth, "r") as f:
            lines = [_.strip("\r\n ").split("\t") for _ in f.readlines()]
        lines = [[l[0], l[1], "1.0", "1.0"] for l in lines]
        f3 = "answer.txt"
        with open(os.path.join(t3, f3), "w") as f:
            f.write("\n".join("\t".join(_) for _ in lines))

        temp = get_temp_folder(__file__, "temp_multi_out")

        # =
        out = os.path.join(temp, "outpute.txt")
        private_codalab_wrapper_multi_classification(AUC_multi_multi,
                                                     ["orientation", "nature"],
                                                     t1, t3, output=out)
        assert os.path.exists(out)
        with open(out, "r") as f:
            code = f.read()

        self.assertEqual(
            code, "orientation_ERR:0.0\norientation_AUC:1.0\nnature_ERR:0.0\nnature_AUC:1.0")

        # dummy
        fLOG("------------ dummy")
        out = os.path.join(temp, "outputd.txt")
        private_codalab_wrapper_multi_classification(AUC_multi_multi,
                                                     ["orientation", "nature"],
                                                     t1, t2, output=out, ignored=["nul"])
        assert os.path.exists(out)
        with open(out, "r") as f:
            code = f.read()
        fLOG("**", code)

        self.assertEqual(
            code, "orientation_ERR:0.7183754333828628\norientation_AUC:0.5862428771453444\nnature_ERR:0.8236750866765725\nnature_AUC:0.5160556240766593")


if __name__ == "__main__":
    unittest.main()
