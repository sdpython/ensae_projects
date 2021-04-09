"""
Measures the performances of the models.
"""
import os
from io import StringIO
import numpy
import json
import pprint
import pandas
import requests
from pyquickhelper.server.filestore_sqlite import SqlLite3FileStore
from ensae_projects.hackathon.random_answers import random_answers_2020_images
from ensae_projects.hackathon.hack2020 import score_images

expected = {
    'test': 'random',
    'tgtg': os.environ.get('TGTG_EXPECTED', '?'),
    'sea': os.environ.get('SEA_EXPECTED', '?'),
}

expected_dfs = {}


def load():
    for k, v in expected.items():
        if os.path.exists(v):
            df = pandas.read_csv(v)
            expected_dfs[k] = df
        elif v == 'random':
            df = random_answers_2020_images().iloc[:, :2]
            expected_dfs[k] = df


def retrieve_missing_metrics(name):
    db = SqlLite3FileStore(name)
    sql = """SELECT files.id FROM files INNER JOIN data ON files.id == data.idfile"""
    sql2 = """SELECT files.id FROM files"""
    cur = db.con_.cursor()
    filled = set(cur.execute(sql))
    allids = set(cur.execute(sql2))
    for ids in allids:
        if ids in filled:
            continue
        sel = """SELECT id, project, content FROM files WHERE id = %s""" % ids

        for id_, proj, content in cur.execute(sel):
            idfile = id_
            metrics = None
            ERRORMSG = None
            if proj not in expected_dfs:
                ERRORMSG = "Project %r must be in list %s." % (
                    proj, list(expected_dfs))
            else:
                df_expected = expected_dfs[proj]
                df = pandas.read_csv(StringIO(content))
                try:
                    metrics = score_images(df_expected, df)
                except Exception as e:
                    ERRORMSG = str(e)
            if ERRORMSG is not None:
                ERRORMSG = ERRORMSG.replace("'", "''")
                db.submit_data(idfile, ERRORMSG, 3.40282e+038)
                continue
            if metrics is None:
                db.submit_data(idfile, "ACC=%f LL=%f" % (
                    metrics['accuracy'], metrics['logloss']), metrics['logloss'])


load()
retrieve_missing_metrics(name)
