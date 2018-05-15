# -*- coding: utf-8 -*-
import sys
import os
# import sphinxjp.themes.basicstrap
# import sphinx_py3doc_enhanced_theme
# import alabaster
import sphinx_redactor_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "ensae_projects", "ENSAE", 2018,
                     "sphinx_redactor_theme",  # "sphinx_py3doc_enhanced_theme",
                     # add_extensions=["alabaster"],
                     sphinx_redactor_theme.get_html_theme_path(), locals(),
                     extlinks=dict(issue=('https://github.com/sdpython/ensae_projects/issues/%s', 'issue')))

# html_theme = 'alabaster'  # 'sphinx_py3doc_enhanced_theme'
# html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
# html_theme_path = [alabaster.get_path()]

blog_root = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/"
blog_background = False

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css'],
}

epkg_dictionary['Cresus'] = "http://www.cresus-france.org/"
epkg_dictionary['data leakage'] = "https://www.kaggle.com/wiki/Leakage"
epkg_dictionary['falcon'] = "https://falconframework.org/"
epkg_dictionary['ijson'] = "https://pypi.python.org/pypi/ijson"
epkg_dictionary['keras'] = "https://keras.io/"
epkg_dictionary['keyring'] = "https://pypi.python.org/pypi/keyring"
epkg_dictionary['Label Emmaüs'] = 'https://www.label-emmaus.co/'
epkg_dictionary['lightmlrestapi'] = "http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/index.html"
epkg_dictionary['REST API'] = "https://en.wikipedia.org/wiki/Representational_state_transfer"
epkg_dictionary['waitress'] = "https://docs.pylonsproject.org/projects/waitress/en/latest/"
epkg_dictionary['WSGI'] = "https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface"
