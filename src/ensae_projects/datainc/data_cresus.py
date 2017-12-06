# -*- coding: utf-8 -*-
"""
@file
@brief Script to process the date from Cresus for the hackathon 2016
"""
import os
import sqlite3
import pandas
from pyquickhelper.loghelper import fLOG
from pyensae.sql import Database


def process_cresus_whole_process(infile, outfold, ratio=0.20, fLOG=fLOG):
    """
    Processes the database from :epkg:`Cresus` until it splits the data into two
    two sets of files.
    """
    if not os.path.exists(outfold):
        os.mkdir(outfold)
    out_clean_sql = os.path.join(
        outfold, os.path.split(infile)[-1] + ".clean.sql")
    outdb = os.path.join(outfold, os.path.split(infile)[-1] + ".db3")
    process_cresus_sql(infile, out_clean_sql=out_clean_sql,
                       outdb=outdb, fLOG=fLOG)
    tables = prepare_cresus_data(outdb, outfold=outfold, fLOG=fLOG)
    train, test = split_train_test_cresus_data(
        tables, outfold, ratio=ratio, fLOG=fLOG)
    nf = split_XY_bind_dataset_cresus_data(test["dossier"], fLOG)
    test.update(nf)
    nf = split_XY_bind_dataset_cresus_data(train["dossier"], fLOG)
    train.update(nf)
    return train, test


def cresus_dummy_file():
    """
    @return     local  filename
    """
    this = os.path.abspath(os.path.dirname(__file__))
    name = os.path.join(this, "hackathon_2016_cresus",
                        "bdd_anonyme_cresus.enc")
    return name


def process_cresus_sql(infile, out_clean_sql=None, outdb=None, fLOG=fLOG):
    """
    Processes the database sent by cresus and produces
    a list of flat files.

    @param      filename        dump of a sql database
    @param      out_clean_sql   filename which contains the cleaned sql
    @param      outdb           sqlite3 file (removed if it exists)
    @param      fLOG            logging function
    @return                     dataframe with a list
    """
    if out_clean_sql is None:
        out_clean_sql = os.path.splitext(infile)[0] + ".cleaned.sql"
    if outdb is None:
        outdb = os.path.splitext(infile)[0] + ".db3"

    dbfile = outdb
    if os.path.exists(dbfile):
        os.remove(dbfile)

    # READING
    fLOG("[process_cresus_sql] reading", infile)
    with open(infile, "r", encoding="utf-8") as f:
        content = f.read()
    fLOG("done")

    # CLEANING
    fLOG("[process_cresus_sql] cleaning")
    lines = content.split("\n")
    repl = [("ENGINE=InnoDB DEFAULT CHARSET=latin1", ""),
            ("CHARACTER SET latin1", ""),
            ("CHARACTER SET utf8", ""),
            ("\\'", "''"),
            ("ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT", ""),
            ("ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8", ""),
            ("ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8", ""),
            ("ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8", ""),
            ("int(11) NOT NULL AUTO_INCREMENT", "INTEGER"),
            ]
    new_lines = []
    modified = 0
    for i, line in enumerate(lines):
        if line.startswith("CREATE DATABASE "):
            line = "-- " + line
            modified += 1
        if line.startswith("USE `cresus_anonyme`"):
            line = "-- " + line
            modified += 1
        for rep, to in repl:
            if rep in line:
                line = line.replace(rep, to)
                modified += 1
        # if line.startswith("REPLACE INTO "):
        #    line = "INSERT" + line[len("REPLACE"):]
        new_lines.append(line)
    content = "\n".join(new_lines)
    fLOG("done l=", len(content), " modified", modified)

    # DATABASE
    fLOG("[process_cresus_sql] execute", dbfile)
    con = sqlite3.connect(dbfile)
    try:
        con.executescript(content)
    except Exception as e:
        try:
            exp = str(e).split('"')[1]
        except Exception:
            raise e
        lines = content.split("\n")
        lines = ["{0}/{2}:{1}".format(i, _, len(lines))
                 for i, _ in enumerate(lines) if exp in _]
        raise Exception("\n".join(lines)) from e
    con.commit()

    # CHECK
    fLOG("[process_cresus_sql] CHECK")
    sql = """SELECT name FROM (SELECT * FROM sqlite_master UNION ALL SELECT * FROM sqlite_temp_master) AS temptbl
             WHERE type in('table','temp') AND name != 'sqlite_sequence' ORDER BY name;"""
    df = pandas.read_sql(sql, con)
    fLOG("[process_cresus_sql]", df)
    fLOG("[process_cresus_sql] done")

    # COUNT
    fLOG("[process_cresus_sql] COUNT")
    sql = " UNION ALL ".join("SELECT \"{0}\" AS name, COUNT(*) AS nb FROM {0}".format(_)
                             for _ in sorted(df.name))
    df = pandas.read_sql(sql, con)
    fLOG("[process_cresus_sql]", df)
    fLOG("[process_cresus_sql] done")

    con.close()

    with open(out_clean_sql, "w", encoding="utf-8") as f:
        f.write(content)

    fLOG("[process_cresus_sql] done")
    return df


def prepare_cresus_data(dbfile, outfold=None, fLOG=fLOG):
    """
    Prepares the data for the challenge.

    @param      dbfile      database file
    @param      outfold     output folder
    @param      fLOG        logging function
    @return                 dictionary of table files
    """
    db = Database(dbfile)
    db.connect()

    if outfold is None:
        outfold = "."

    remove_column = ['nom', 'prenom',
                     'tel_fixe', 'tel_mobile', 'email',
                     'adresse', 'rdv1', 'rdv2', 'rdv3',
                     'fichier_suivi', 'fichier_suivi2', 'media',
                     'indicateur_suivi', 'memo', 'num_dossier',
                     'etat_old', 'orientation_old', 'indicateur_suivi_old',
                     'transfert', 'plan_bdf', 'effacement_dett', "etat",
                     #
                     'tel_fixe', 'tel_port',
                     ]

    new_mapping = {'': 'nul1', None: 'nul2',
                   'Sur-endettement': 'Surendettement', '0': 'nul'}

    res = {}
    tables = db.get_table_list()
    for table in tables:
        fLOG("[prepare_cresus_data] exporting", table)
        df = pandas.read_sql("select * from " + table, db._connection)
        cols = [_ for _ in df.columns if _ not in remove_column]
        cols.sort()
        if "orientation" in cols:
            cols = [_ for _ in cols if _ not in ("orientation", "nature")]
            cols += ["orientation", "nature"]
            df["nature"] = df.nature.apply(
                lambda x: new_mapping.get(x, x).replace("Ã©", "e").lower())
            fLOG(set(df["nature"]))
        df = df[cols]
        name = os.path.join(outfold, "tbl_" + table + ".txt")
        df.to_csv(name, sep="\t", encoding="utf-8", index=False)
        res[table] = name
    db.close()
    return res


def split_train_test_cresus_data(tables, outfold, ratio=0.20, fLOG=fLOG):
    """
    Splits the tables into two sets for tables (based on users).

    @param          tables      dictionary of tables,
                                @see fn prepare_cresus_data
    @param          outfold     if not None, output all tables in this folder
    @param          fLOG        logging function
    @return                     couple of dictionaries of table files
    """
    splits = ["user", "agenda", "dossier", "budget"]
    df = pandas.read_csv(tables["dossier"], sep="\t", encoding="utf-8")
    short = df[["id", "id_user", "date_ouverture"]
               ].sort_values("date_ouverture")
    nb = len(short)
    train = int(nb * (1 - ratio))
    dossiers = set(short.loc[:train, "id"])
    users = set(short.loc[:train, "id_user"])

    train_tables = {}
    test_tables = {}
    for k, v in tables.items():
        if k not in splits:
            fLOG("[split_train_test_cresus_data] no split for", k)
            data = pandas.read_csv(v, sep="\t", encoding="utf-8")
            train_tables[k] = data
            test_tables[k] = data
        else:
            if k == "dossier":
                train_tables[k] = df[:train].copy()
                test_tables[k] = df[train:].copy()
            else:
                data = pandas.read_csv(v, sep="\t", encoding="utf-8")
                if "id_dossier" in data.columns:
                    key = "id_dossier"
                    select = dossiers
                elif k == "user":
                    key = "id"
                    select = users
                else:
                    raise Exception("unexpected: {0}".format(k))
                try:
                    spl = data[key].apply(lambda x: x in select)
                except KeyError as e:
                    raise Exception("issue for table '{0}' and columns={1}".format(
                        k, data.columns)) from e
                train_tables[k] = data[spl].copy()
                test_tables[k] = data[~spl].copy()
            fLOG("[split_train_test_cresus_data] split for", k,
                 train_tables[k].shape, test_tables[k].shape)

    rtrain = {}
    for k, v in train_tables.items():
        name = os.path.join(outfold, "tbl_train_" + k + ".txt")
        v.to_csv(name, index=False, sep="\t", encoding="utf-8")
        rtrain[k] = name
    rtest = {}
    for k, v in test_tables.items():
        name = os.path.join(outfold, "tbl_test_" + k + ".txt")
        v.to_csv(name, index=False, sep="\t", encoding="utf-8")
        rtest[k] = name
    return rtrain, rtest


def split_XY_bind_dataset_cresus_data(filename, fLOG=fLOG):
    """
    Splits XY for the blind set.

    @param      filename        table to split
    @return                     dictionary of created files

    It assumes the targets are columns *orientation*, *nature*.
    """
    df = pandas.read_csv(filename, sep="\t", encoding="utf-8")
    isnull = df["orientation"].isnull() | df["nature"].isnull()
    df = df[~isnull]
    X = df.drop(["orientation", "nature"], axis=1)
    Y = df[["orientation", "nature"]]
    xname = os.path.splitext(filename)[0] + ".X.txt"
    yname = os.path.splitext(filename)[0] + ".Y.txt"
    X.to_csv(xname, sep="\t", index=False, encoding="utf-8")
    Y.to_csv(yname, sep="\t", index=False, encoding="utf-8")
    return {"dossier.X": xname, "dossier.Y": yname}
