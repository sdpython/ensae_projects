#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
#import sphinxjp.themes.basicstrap
import sphinx_bootstrap_theme

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
                     "bootstrap",
                     None,
                     locals(),
                     add_extensions=None)

html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_logo = "project_ico_small.png"
language = "fr"

html_sidebars = {}

if html_theme == "bootstrap":
    html_theme_options = {
        'navbar_title': "home",
        'navbar_site_name': "Site",
        'navbar_links': [
            ("XD", "http://www.xavierdupre.fr", True),
            ("ENSAE",
             "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/index.html", True),
            ("module", "py-modindex"),
            ("index", "genindex"),
        ],
        'navbar_sidebarrel': False,
        'navbar_pagenav': True,
        'navbar_pagenav_name': "Page",
        'globaltoc_depth': 3,
        'globaltoc_includehidden': "true",
        'navbar_class': "navbar navbar-inverse",
        'navbar_fixed_top': "true",
        'source_link_position': "nav",
        'bootswatch_theme': "slate",
        # united = weird colors, sandstone=green, simplex=red, paper=trop bleu
        # lumen: OK
        # to try, yeti, flatly, paper
        'bootstrap_version': "3",
    }

blog_root = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/"
blog_background = False
