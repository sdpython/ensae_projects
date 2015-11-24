#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
#import sphinxjp.themes.basicstrap
import sphinx_py3doc_enhanced_theme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src")))

from pyquickhelper.helpgen.default_conf import set_sphinx_variables

set_sphinx_variables(__file__,
                     "ensae_projects",
                     "ENSAE",
                     2015,
                     "sphinx_py3doc_enhanced_theme",
                     None,
                     locals(),
                     add_extensions=None)

html_theme = 'sphinx_py3doc_enhanced_theme'
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]

blog_root = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/"
blog_background = False
