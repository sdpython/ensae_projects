"""
@file
@brief Data related to La Croix-Rouge (Hackathon Microsoft / ENSAE / Croix-Rouge / 2015)
"""
import os
import pandas
from .data_exception import ProjectDataException


def get_meaning(table="invoice"):
    """
    retrieve data related to the meaning of a table

    @param      table       invoice or ...
    @return                      DataFrame
    """
    fold = os.path.abspath(os.path.dirname(__file__))
    if table == "invoice":
        name = os.path.join(fold, "meaning_invoice.txt")
        df = pandas.read_csv(name, sep="\t", encoding="utf-8")
        df.columns = [_.strip() for _ in df.columns]
        for c in df.columns:
            df[c] = df[c].apply(lambda s: s.strip())
        return df
    else:
        raise ProjectDataException(
            "unable to find information about table {0}".format(table))
