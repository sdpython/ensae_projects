"""
@file
@brief Compute the performance for the hackathon 2018.
"""
import os
import time
import pandas
import numpy
from PIL import Image
from lightmlrestapi.mlapp.mlstorage import MLStorage
try:
    from ..hackathon.image_helper import enumerate_image_class
except (ImportError, ValueError):
    from ensae_projects.hackathon.image_helper import enumerate_image_class


class MLStoragePerf2018:
    """
    Computes the performances the a hackathon.
    """

    def __init__(self, storage, examples, cache_file="cache_file.csv"):
        """
        @param      storage     storage location
        @param      examples    deep learning models
        """
        self._storage = self._load_ml_storage(storage)
        self._examples = examples
        self._cache_file = cache_file

    def _load_ml_storage(self, root):
        """
        Creates an instance of a
        `MLStorage <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/lightmlrestapi/mlapp/mlstorage.html
        # lightmlrestapi.mlapp.mlstorage.MLStorage>`_
        based on a folder.

        @param      root        folder
        """
        if not os.path.exists(root):
            raise FileNotFoundError("Unable to find '{0}'".format(root))
        stor = MLStorage(root)
        return stor

    def _load_cached_performance(self, cache_file=None):
        """
        Retrieves performances already computed.

        @param      cached_file     file
        """
        if cache_file is None:
            cache_file = self._cache_file
        if os.path.exists(cache_file):
            df = pandas.read_csv(cache_file, sep=",", encoding="utf-8")
            return df
        else:
            return None

    def _save_performance(self, df, cache_file=None):
        """
        Saves cached performance.

        @param      df          dataframe
        @param      cache_file  destination
        """
        if cache_file is None:
            cache_file = self._cache_file
        df.to_csv(cache_file, sep=',', encoding='utf-8', index=False)

    def compute_performance(self, use_cache=True, fLOG=None):
        """
        Computes the performance for the not cached one if
        *use_cache* is True.

        @param      use_cache   use cache
        @param      fLOG        logging function
        @return     dataframe
        """
        cache = None
        already = set()
        if use_cache:
            cache = self._load_cached_performance()
            if cache is not None:
                already = set(cache["name"])

        rows = []
        for i, name in enumerate(sorted(self._storage.enumerate_names())):
            if i % 30 == 0:
                print('.')
            if name not in already:
                t0 = time.perf_counter()
                if fLOG:
                    fLOG(
                        "[MLStoragePerf2018] compute perf for {0}: '{1}'".format(i, name))
                res = self.compute_perf(name)  # pylint: disable=E1111
                if fLOG:
                    fLOG(
                        "[MLStoragePerf2018] Done for {0}: {1}".format(name, res))
                    if 'exc' in res:
                        fLOG("[MLStoragePerf2018] exception for {0}: {1}".format(
                            name, res['exc']))
                res["name"] = name
                res["stime"] = os.stat(self._storage._folder, name).st_mtime
                t1 = time.perf_counter() - t0
                res["time"] = t1
                rows.append(res)
                already.add(name)

        df = pandas.DataFrame(rows)
        sc = list(sorted(df.columns))
        df = df[sc]

        if cache is not None:
            df = pandas.concat([df, cache])

        df = df.sort_values("name").copy()

        self._save_performance(df)

        return df

    def compute_perf(self, name):
        """
        Computes the performances for every image and one
        particular model.
        """
        raise NotImplementedError()


class MLStoragePerf2018Image(MLStoragePerf2018):
    """
    Overloads *compute_perf* for images.
    Example of use:

    ::

        from ensae_projects.hackathon.perf2018 import MLStoragePerf2018Image
        mstorage = "storage_brgm"
        mexample = "hackathon_test/sample_labelled_test"
        mpref = MLStoragePerf2018Image(mstorage, mexample)
        mres = mpref.compute_performance(fLOG=print, use_cache=True)
        mres = mres.sort_values("precision", ascending=False)
        print(mres)
        mbody = "<html><body><h1>Hackathon EY-ENSAE 2018 - BRGM</h1>\n"
        mcontent = "{0}{1}</body></html>".format(mbody, mres.to_html())
        with open("brgm.html", "w", encoding="utf-8") as f:
            f.write(mcontent)
    """

    def __init__(self, storage, examples, cache_file="cache_file.csv"):
        """
        @param      storage     storage location
        @param      examples    deep learning models
        """
        MLStoragePerf2018.__init__(self, storage, examples, cache_file)

    def _label_mapping(self, subs):
        """
        Computes the label based on a subfolder name.
        """
        return 1 if subs.endswith('1') else 0

    def compute_perf(self, name):
        """
        Computes the performances for every image and one
        particular model.
        """
        from keras import backend as K
        K.clear_session()
        folder = self._examples

        try:
            model = self._storage.load_model(name)
            vers = self._storage.call_version(name)
            exc = None
        except Exception as e:  # pylint: disable=W0703
            model = None
            exc = e
            vers = None

        rows = []
        for img, sub in enumerate_image_class(folder):
            label = self._label_mapping(sub)
            obs = dict(image=img, sub=sub, label=label)
            if model is None:
                obs = {'exc': Exception("model is None")}
                pred = None
            else:
                X = numpy.array(Image.open(img))
                try:
                    pred = self._storage.call_predict(
                        name, X, loaded_model=model)
                    # print("*****",pred)
                except Exception as e:  # pylint: disable=W0703
                    exc = e
                    pred = None
                    #print('------', e)

            if pred is None:
                pass
            else:
                if isinstance(pred, float):
                    plabel = 1 if pred > 0.5 else 0
                    score = pred
                if isinstance(pred, list):
                    pred = numpy.array(pred)
                if isinstance(pred, numpy.ndarray):
                    pred = pred.ravel()
                    if len(pred) == 1:
                        plabel = 1 if pred[0] > 0.5 else 0
                        score = pred[0]
                    elif len(pred) > 1:
                        plabel = numpy.argmax(pred)
                        score = pred[plabel]
                    else:
                        exc = ValueError("No prediction")
                else:
                    exc = TypeError(
                        "Prediction with the wrong type {0}".format(type(pred)))

            if exc:
                obs.update({'exc': exc})
            else:
                obs.update(dict(predicted_label=plabel, score=score))

            rows.append(obs)
            # print(rows)
            # break

        final = pandas.DataFrame(rows)
        columns = list(final.columns)
        if 'score' in columns:
            final["score"] = final["score"].fillna(0)
            final["predicted_label"] = final["predicted_label"].fillna(-1)
            final["correct"] = final["predicted_label"] == final["label"]
            final["correcti"] = 0
            final.loc[final["correct"], "correcti"] = 1

            res = {}
            if exc:
                res["exc"] = str(exc)
            if len(final) > 0:
                gr = final["correcti"].sum() / final.shape[0]
                res["precision"] = gr

                gr = final[["sub", "correcti", "correct"]]
                gr = gr.groupby("sub", as_index=False)
                gr = gr.agg({"correct": len, 'correcti': sum})
                gr["ratio"] = gr["correcti"] / gr["correct"]
                for i in range(gr.shape[0]):
                    res["p_%s" % gr.loc[i, "sub"]] = gr.loc[i, "ratio"]
            else:
                res["precision"] = 0
        else:
            res = dict(exc=exc, precision=0)

        if vers is not None:
            res["version"] = vers
        return res


class MLStoragePerf2018TimeSeries(MLStoragePerf2018):
    """
    Overloads *compute_perf* for timeseries.

    Example of use:

    ::

        from ensae_projects.hackathon.perf2018 import MLStoragePerf2018TimeSeries
        mstorage = "storage_microdon"
        mexample = "hackathon_test/sample_labelled_test"
        mpref = MLStoragePerf2018TimeSeries(mstorage, mexample)
        mres = mpref.compute_performance(fLOG=print, use_cache=True)
        mres = mres.sort_values("cor", ascending=False)
        print(mres)
        mbody = "<html><body><h1>Hackathon EY-ENSAE 2018 - Microdon</h1>\n"
        mcontent = "{0}{1}</body></html>".format(mbody, mres.to_html())
        with open("brgm.html", "w", encoding="utf-8") as f:
            f.write(mcontent)
    """

    def __init__(self, storage, examples, cache_file="cache_file.csv"):
        """
        @param      storage     storage location
        @param      examples    deep learning models
        """
        MLStoragePerf2018.__init__(self, storage, examples, cache_file)

        df = pandas.read_csv(examples)

        sub = df[["year", "week", "campaigns_campaign_id", "collecteur_id",
                  "montant_total", "nb_dons_total", "nb_transac_total"]].copy()
        dsub = sub.fillna(0)
        gr = dsub.groupby(
            ["year", "week", "campaigns_campaign_id"], as_index=False).sum()
        gr["PARTICIPATION"] = gr["nb_dons_total"] / gr["nb_transac_total"]
        self._expected = gr

    def _label_mapping(self, subs):
        """
        Computes the label based on a subfolder name.
        """
        return 1 if subs.endswith('1') else 0

    def compute_perf(self, name):
        """
        Computes the performances for every image and one
        particular model.
        """

        try:
            model = self._storage.load_model(name)
            vers = self._storage.call_version(name)
            exc = None
        except Exception as e:  # pylint: disable=W0703
            model = None
            exc = e
            vers = None

        cols = ["year", "week", "campaigns_campaign_id",
                "PARTICIPATION", "nb_transac_total"]
        X = self._expected[cols]
        total = 0
        total10 = 0
        total100 = 0
        total1000 = 0
        n1 = 0
        n10 = 0
        n100 = 0
        n1000 = 0

        preds = []
        exps = []
        diffs = {}

        for i in range(0, X.shape[0]):
            week = X.iloc[i, 1]
            camp = X.iloc[i, 2]
            exp = X.iloc[i, 3]
            if exp > 1:
                continue
            nb_transac_total = X.iloc[i, 4]
            if nb_transac_total > 0:
                try:
                    pred = self._storage.call_predict(
                        name, (week, camp), loaded_model=model)
                except Exception as e:  # pylint: disable=W0703
                    exc = e
                    pred = 0
                if isinstance(pred, list):
                    if len(pred) == 1:
                        pred = pred[0]
                    else:
                        exc = Exception(
                            "Returned a list of value when expecting one")
                elif isinstance(pred, numpy.ndarray):
                    pred = pred.ravel()
                    if len(pred) == 1:
                        pred = pred[0]
                    else:
                        exc = Exception(
                            "Returned a list of value when expecting one")
                n1 += 1
                exps.append(exp)
                preds.append(pred)
                diffs[week, camp] = abs(exp - pred)
                total += (pred - exp) ** 2
                if nb_transac_total >= 10:
                    total10 += (pred - exp) ** 2
                    n10 += 1
                    if nb_transac_total >= 100:
                        total100 += (pred - exp) ** 2
                        n100 += 1
                        if nb_transac_total >= 1000:
                            total1000 += (pred - exp) ** 2
                            n1000 += 1

        res = {}
        if vers is not None:
            res["version"] = vers
        if exc is not None:
            res["exc"] = exc
        if n1 > 0:
            res["score"] = (total / n1) ** 0.5
            res["score10"] = (total10 / n10) ** 0.5
            res["score100"] = (total100 / n100) ** 0.5
            res["score1000"] = (total1000 / n1000) ** 0.5
            try:
                res["cor"] = numpy.corrcoef(numpy.array(preds),
                                            numpy.array(exps))[0, 1]
            except (AttributeError, KeyError):
                res["cor"] = numpy.nan
            try:
                res["pmin"] = numpy.min(preds)
                res["pmax"] = numpy.max(preds)
            except (KeyError, ValueError):
                res["pmin"] = numpy.nan
                res["pmax"] = numpy.nan

            resort = [(v, k) for k, v in diffs.items()]

            try:
                resort.sort()
                skip = False
            except ValueError:
                skip = True
                exc = Exception(
                    "Unable to sort differences {0}".format(resort[0]))
            if not skip:
                last = resort[-1]
                res["worst"] = "{0}:{1}".format(last[1], last[0])
                best = resort[0]
                res["best"] = "{0}:{1}".format(best[1], best[0])
        return res


if __name__ == "__main__":
    mstorage = r'/home/jbr/hack35/'
    mexample = r'./sample_labelled_test'
    mpref = MLStoragePerf2018Image(mstorage, mexample)
    mres = mpref.compute_performance(fLOG=print, use_cache=True)
    mres = mres.sort_values("precision", ascending=False)
    print(mres)
    if 'exc' in mres.columns:
        print(list(mres['exc']))
    mbody = "<html><body><h1>Hackathon EY-ENSAE 2018 - BRGM</h1>\n"
    mcontent = "{0}{1}</body></html>".format(mbody, mres.to_html())
    from pyquickhelper.pandashelper.tblformat import df2rst
    with open("hackathon2018/brgm.rst", "w", encoding="utf-8") as f:
        f.write(df2rst(mres))
    with open("hackathon2018/brgm.html", "w", encoding="utf-8") as f:
        f.write(mcontent)
