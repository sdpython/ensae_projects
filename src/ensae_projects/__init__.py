# -*- coding: utf-8 -*-
"""
@file
@brief Module *ensae_projects*.
Compilation of materials for presentations.
"""

import sys
import os

__version__ = "0.2.593"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/ensae_projects"
__url__ = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/index.html"
__license__ = "MIT License"
__blog__ = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "rss_ensae_projects.xml"))


def _setup_hook():
    """
    does nothing
    """
    pass


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True
