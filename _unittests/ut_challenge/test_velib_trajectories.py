# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
import pandas
from pyquickhelper.pycode import get_temp_folder
from pyquickhelper.loghelper import fLOG, str2datetime


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


from src.ensae_projects.challenge.velib_trajectories import get_data, enumerate_events, appariement
from src.ensae_projects.challenge.velib_trajectories import ParemetreCoutTrajet, distance_path


class TestVelibTrajectories(unittest.TestCase):

    def test_velib(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        dest = get_temp_folder(__file__, "temp_velib_trajectories")
        get_data(dest)

        # récupère les données
        jeu = os.path.join(dest, "besancon.df.txt")
        jeu = os.path.join(dest, "out_simul_bike_nb1_sp10_data.txt")
        df = pandas.read_csv(jeu, sep="\t", encoding="utf8")
        # conversion des dates
        df["collect_date"] = df.apply(
            lambda r: str2datetime(r["collect_date"]), axis=1)
        # fLOG(df.head())

        # on regarde s'il existe le fichier des trajectoires
        path = jeu.replace("_data.", "_path.")
        if path != jeu and os.path.exists(path):
            dfp = pandas.read_csv(path, sep="\t")
            dfp = dfp[dfp["beginend"] == "end"]
            mean, std = distance_path(dfp)
            fLOG("expected: vitesse moyenne ", mean, " stddev ", std)

        # on calcule les événements (1 vélo apparu, 1 vélo disparu)
        events = list(sorted(enumerate_events(df)))

        params = ParemetreCoutTrajet()
        fLOG(params)
        mindist, moyenne, appariement_, positif, negatif = appariement(
            events, iter=100, params=params)
        fLOG("vitesse moyenne", moyenne)
        self.assertGreater(moyenne, 0)
        self.assertLess(moyenne, 10)


if __name__ == "__main__":
    unittest.main()
