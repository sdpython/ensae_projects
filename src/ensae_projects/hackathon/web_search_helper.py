# -*- coding: utf-8 -*-
"""
@file
@brief Helpers for the hackathon 2018 related to search internet.
"""


import urllib
import urllib.request
import urllib.parse
import time
import random
import re
import os


def extract_bing_result(search_page, filter_fct=lambda u: True):
    """
    Extract the first results from a search page assuming
    it comes from :epkg:`Bing Image`.

    @param      search_page     content of :epkg:`Bing Image` search page (or filename)
    @param      filter_fct      remove some urls if this function is False ``filter(u) --> True or False``
    @return                     a list with the urls
    """
    if search_page.endswith(".html"):
        with open(search_page, "r", encoding="utf-8") as f:
            search_page = f.read()
    reg = re.compile("""mediaurl=(http.*?)&""")
    res = reg.findall(search_page)
    if res is None or len(res) == 0:
        reg = re.compile('''href="(http.*?)"''')
        res = reg.findall(search_page)
        ext = {'.jpg', '.png', '.gif', '.tif'}
        res = [_ for _ in res if len(_) > 4 and _[-4:] in ext]
    return list(urllib.parse.unquote(_) for _ in set(filter(filter_fct, res)))


def query_bing_image(query, folder_cache="cache_search_page",
                     filter_fct=lambda u: True, add_options=False,
                     use_selenium=False, navigator=None, fLOG=None):
    """
    Returns the search page from :epkg:`Bing Image`
    for a specific query.

    @param      query           search query
    @param      folder_cache    folder used to stored the result page or to retrieve
                                a page if the query was already searched for
    @param      filter_fct      remove some urls if this function is False
                                ``filter(u) --> True or False``
    @param      add_options     add options to the search url
    @param      use_selenium    relies on :epkg:`webhtml`
    @param      navigator       see :epkg:`webhtml`
    @param      fLOG            logging function
    @return                     list of urls
    """
    if not os.path.exists(folder_cache):
        os.mkdir(folder_cache)
    cache = os.path.join(folder_cache, "%s.bing.html" %
                         query.replace(" ", "_"))
    if os.path.exists(cache):
        with open(cache, "r", encoding="utf8") as f:
            text = f.read()
    else:
        if fLOG:
            fLOG("[query_bing_image] download results for '{0}'".format(query))
        x = 1. + random.random()
        time.sleep(x)
        encoded = urllib.parse.quote(query)
        if add_options:
            uopts = "&qs=n&form=QBIR&sp=-1&sc=8-10&sk="
        else:
            uopts = ""

        url = "http://www.bing.com/images/search?q={0}{1}".format(
            encoded, uopts)

        if use_selenium:
            from ensae_teaching_cs.faq.faq_web import webhtml
            if navigator is None:
                navigator = "chrome"
            res = webhtml(url, navigator=navigator)
            if len(res) == 0:
                return None
            text = res[0][1]
        else:
            with urllib.request.urlopen(url, timeout=10) as uur:
                text = uur.read()
            text = text.decode("utf8")

        if fLOG:
            fLOG("[query_bing_image] cache results for '{0}' in '{1}'".format(
                query, cache))
        with open(cache, "w", encoding="utf-8") as f:
            f.write(text)

    urls = extract_bing_result(text, filter_fct)
    return urls
