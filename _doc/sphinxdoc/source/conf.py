#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
#import sphinxjp.themes.basicstrap
# import sphinx_py3doc_enhanced_theme
import alabaster

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

set_sphinx_variables(__file__, "ensae_projects", "ENSAE", 2016,
                     "alabaster",  # "sphinx_py3doc_enhanced_theme",
                     None, locals(), add_extensions=["alabaster"],
                     extlinks=dict(issue=('https://github.com/sdpython/ensae_projects/issues/%s', 'issue')))

html_theme = 'alabaster'  # 'sphinx_py3doc_enhanced_theme'
# html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
html_theme_path = [alabaster.get_path()]

blog_root = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/"
blog_background = False

html_context = {
    'css_files': ['_static/my-styles.css'],
}
