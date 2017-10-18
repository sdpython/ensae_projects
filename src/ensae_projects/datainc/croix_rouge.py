#-*- coding: utf-8 -*-
"""
@file
@brief Data related to La Croix-Rouge (Hackathon Microsoft / ENSAE / Croix-Rouge / 2015)
"""
import os
import pandas
import io
import warnings
from pyquickhelper.filehelper import encrypt_stream, decrypt_stream
from pyquickhelper.pandashelper import df2rst, df2html
from .data_exception import ProjectDataException, PasswordException


def get_password_from_keyring_or_env(pwd):
    """
    Get the password from `keyring <https://pypi.python.org/pypi/keyring>`_ first,
    then from the environment variables.

    @param      pwd     password to use or None to get it as ``os.environ["PWDCROIXROUGE"]``
                        or from `keyring <https://pypi.python.org/pypi/keyring>`_.
    @return             password

    To set the password for `keyring <https://pypi.python.org/pypi/keyring>`_:

    ::

        keyring.set_password("HACKATHON2015", "PWDCROIXROUGE", "value")
    """
    if pwd is None:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            import keyring
        pwd = keyring.get_password("HACKATHON2015", "PWDCROIXROUGE")
        if pwd is None:
            if "PWDCROIXROUGE" not in os.environ:
                raise PasswordException(
                    "password not found in environment variables: PWDCROIXROUGE is not set")
            else:
                pwd = os.environ["PWDCROIXROUGE"]
        return bytes(pwd, encoding="ascii")
    elif not isinstance(pwd, bytes):
        return bytes(pwd, encoding="ascii")
    else:
        return pwd


def encrypt_file(infile, outfile, password=None):
    """
    Encrypt a file with a specific password.

    @param      password        password for the hackathon, if None, look into
                                ``os.environ["PWDCROIXROUGE"]``
    @param      infile          input file
    @param      outfile         output file
    @return                     outfile
    """
    password = get_password_from_keyring_or_env(password)
    return encrypt_stream(password, infile, outfile)


def decrypt_dataframe(infile, password=None, sep="\t", encoding="utf8", **kwargs):
    """
    Read an encrypted dataframe.

    @param      infile      filename
    @param      password    password
    @param      sep         separator
    @param      encoding    encoding
    @param      kwargs      others options for `read_csv <>`_
    @return                 dataframe
    """
    password = get_password_from_keyring_or_env(password)
    data = decrypt_stream(password, infile)
    st = io.BytesIO(data)
    df = pandas.read_csv(st, sep=sep, encoding="utf8", **kwargs)
    return df


def get_meaning(table="invoice", password=None):
    """
    Retrieve data related to the meaning of a table.

    @param      table           SINVOICE or SINVOICE_V, ITTMASTER or stojou
    @param      password        password, see @see fn get_password_from_keyring_or_env
    @return                     DataFrame
    """
    fold = os.path.abspath(os.path.dirname(__file__))
    if table == "invoice":
        name = os.path.join(
            fold, "hackathon_2015_croix_rouge", "meaning_invoice.enc")
        df = decrypt_dataframe(name, password=password)
        df.columns = [_.strip() for _ in df.columns]
        for c in df.columns:
            df[c] = df[c].apply(lambda s: s.strip())
        df.columns = ["Zone"] + list(df.columns[1:])
        return df
    elif table in {"ITMMASTER", "SINVOICE", "SINVOICE_V", "stojou"}:
        name = os.path.join(
            fold, "hackathon_2015_croix_rouge", "%s.schema.enc" % table)
        df = decrypt_dataframe(name, password=password,
                               sep="," if "stojou" in table else "\t")
        if table in "ITMMASTER":
            df["Zone"] = df.index + 1
            df["Zone"] = df.Zone.apply(lambda x: "ITM_%03d" % x)
        df.columns = [_.strip() for _ in df.columns]
        # we remove column always null
        df = df.dropna(axis=1, how='all')
        return df
    else:
        raise ProjectDataException(
            "unable to find information about table {0}".format(table))


def merge_schema(tables=None, password=None):
    """
    Merges schemas of various databases.

    @param      tables      list of tables or None for all
    @param      password    password
    @return                 dataframe with all columns
    """
    if tables is None:
        tables = ["invoice", "ITMMASTER", "SINVOICE", "SINVOICE_V", "stojou"]

    dfs = [get_meaning(tbl, password=password) for tbl in tables]
    for df, name in zip(dfs, tables):
        df["name"] = name

    join = None
    for name, df in sorted(zip(tables, dfs)):
        nickname = name[0] + name[-1]
        df = df.copy()
        df.columns = [c + "_" + nickname if c !=
                      "Zone" else c for c in df.columns]
        if join is None:
            join = df
        else:
            join = join.merge(df, on="Zone", how="outer",
                              suffixes=("", "_" + nickname))

    # we merge what can be merged
    def merge_values(row, cs):
        return", ".join(list(set(row[c] for c in cs if isinstance(row[c], str))))

    for prf in "Typ,Menu,Long,Dim,Act,Intitulé long,Table liée,Expression de lien,Vérification,Obligatoire,RAZ".split(","):
        cs = [c for c in join.columns if c.startswith(prf)]
        if prf == "Intitulé long":
            cs.append("Description_ie")
        new_col = join.apply(lambda row: merge_values(row, cs), axis=1)
        join = join[[c for c in join.columns if c not in cs]]
        join[prf] = new_col

    cols = "Zone,name_ie,name_IR,name_SE,name_SV,name_su,Intitulé long" + \
           ",Typ,Menu,Long,Act,Dim,Table liée,Expression de lien,Vérification,Obligatoire,RAZ"
    cols = cols.split(",")
    join = join.sort_values("Zone")
    join = join[cols]
    join = join.reset_index(drop=True)
    join = join.reset_index(drop=False)
    return join


def df2rsthtml(df, format="html", fillna=""):
    """
    Writes a table into RST or HTML format.

    @param      df          dataframe
    @param      format      format
    @param      fillna      fill empty values
    @return                 string
    """
    df = df.fillna(fillna)
    if format == "html":
        return df2html(df)
    elif format == "rst":
        return df2rst(df)
