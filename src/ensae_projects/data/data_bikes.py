#-*- coding: utf-8 -*-
"""
@file
@brief Data related to a challenge, streets in Seattle
"""
import os
import pandas
from datetime import time
from pyensae.datasource import download_data
from pyensae.notebook_helper import folium_html_map


def get_chicago_stations(folder=".", as_df=False):
    """
    Retrieve processed data from
    `Divvy Data <https://www.divvybikes.com/system-data>`_.

    @param      folder          temporary folder where to download files
    @param      as_df
    @return                     filename or 2 dataframes (`as_df=True`)
    """
    file = download_data("Divvy_Trips_2016_Q3Q4.zip",
                         url="https://s3.amazonaws.com/divvy-data/tripdata/",
                         whereTo=folder)
    if as_df:
        df1 = pandas.read_csv(os.path.join(
            folder, "Divvy_Stations_2016_Q3.csv"))
        df2 = pandas.read_csv(os.path.join(folder, "Divvy_Trips_2016_Q3.csv"))
        df3 = pandas.read_csv(os.path.join(folder, "Divvy_Trips_2016_Q4.csv"))
        df34 = pandas.concat([df2, df3])
        return df1, df34
    else:
        return file


def df_crossjoin(df1, df2, **kwargs):
    """
    Make a cross join (cartesian product) between two dataframes by using a constant temporary key.
    Also sets a MultiIndex which is the cartesian product of the indices of the input dataframes.
    Source: `Cross join / cartesian product between pandas DataFrames <https://mkonrad.net/2016/04/16/cross-join--cartesian-product-between-pandas-dataframes.html>`_

    @param      df1     dataframe 1
    @param      df2     dataframe 2
    @param      kwargs  keyword arguments that will be passed to pd.merge()
    @return             cross join of df1 and df2
    """
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1
    res = pandas.merge(df1, df2, on='_tmpkey', **
                       kwargs).drop('_tmpkey', axis=1)
    res.index = pandas.MultiIndex.from_product((df1.index, df2.index))
    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)
    return res


def add_missing_time(df, column, values, delay=10):
    """
    After aggregation, it usually happens that the series is sparse.
    This function add rows for missing time.

    @param      df      dataframe to extend
    @param      column  column with time
    @param      values  columns which contain the values, the others are considered as the keys
    @aram       dely    populate every *delay* minute
    @return             new dataframe
    """
    if isinstance(values, str):
        values = [values]
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    all_times = [time(i // 60, i % 60, 0) for i in range(0, 24 * 60, delay)]
    keys = [_ for _ in df.columns if _ not in values and _ != column]
    dfti = pandas.DataFrame({column: all_times})
    only = df[keys + [column]
              ].groupby(keys, as_index=False).count().drop(column, axis=1)
    dfti = df_crossjoin(only, dfti)
    dfj = df.merge(dfti, on=keys + [column], how="right")
    for i in range(dfj.shape[1]):
        if dfj.dtypes[i] != object:
            dfj[dfj.columns[i]].fillna(0, inplace=True)
    return dfj.sort_values(column)


def folium_html_stations_map(stations, html_width=None, html_height=None, **kwargs):
    """
    Returns a folium map which shows stations in different colors.

    @param      stations        list ``[ (lat, lon), color ]`` or ``[ (lat, lon), (name, color) ]``
    @param      kwargs          extra parameters for `Map <https://github.com/python-visualization/folium/blob/master/folium/folium.py#L19>`_
    @param      html_width      sent to function
                                `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    @param      html_height     sent to function
                                `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    @return                     see function
                                `folium_html_map <http://www.xavierdupre.fr/app/pyensae/helpsphinx/pyensae/notebook_helper/folium_helper.html#pyensae.notebook_helper.folium_helper.folium_html_map>`_
    """
    import folium
    map_osm = None
    for key, value in stations:
        x, y = key
        if map_osm is None:
            if "zoom_start" not in kwargs:
                kwargs["zoom_start"] = 11
            if "location" not in kwargs:
                map_osm = folium.Map(location=[x, y], **kwargs)
            else:
                map_osm = folium.Map(kwargs["location"], **kwargs)
        if isinstance(value, tuple):
            name, value = value
            map_osm.add_child(folium.CircleMarker(
                [x, y], popup=name, radius=15, fill_color=value, color=value))
        else:
            map_osm.add_child(folium.CircleMarker(
                [x, y], radius=15, fill_color=value, color=value))
    return folium_html_map(map_osm, width=html_width, height=html_height)
