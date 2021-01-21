# -*- coding: utf-8 -*-
import sys
import os
import pydata_sphinx_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "ensae_projects", "ENSAE", 2021,
                     "pydata_sphinx_theme", pydata_sphinx_theme.get_html_theme_path(),
                     locals(),
                     extlinks=dict(issue=('https://github.com/sdpython/ensae_projects/issues/%s', 'issue')))

html_theme_options = {
    'navbar_title': "BASE",
    'navbar_site_name': "Site",
    'navbar_links': [
        ("XD", "http://www.xavierdupre.fr", True),
        ("blog", "blog/main_0000.html", True),
        ("index", "genindex"),
    ],
    'navbar_sidebarrel': True,
    'navbar_pagenav': True,
    'navbar_pagenav_name': "Page",
    'bootswatch_theme': "readable",
    'bootstrap_version': "3",
    'source_link_position': "footer",
}

blog_root = "http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/"
blog_background = False
pygments_style = 'default'
html_logo = "phdoc_static/project_ico_small.png"

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css'],
}

epkg_dictionary.update({
    'API REST': 'https://fr.wikipedia.org/wiki/Representational_state_transfer',
    'B-Corp': "https://bcorporation.eu/about-b-lab/country-partner/france",
    'Bing Image': 'https://www.bing.com/images/',
    'BRGM': "http://www.brgm.fr/",
    'cartopy': "https://scitools.org.uk/cartopy/docs/latest/",
    'Cancer Imaging Archive': 'https://wiki.cancerimagingarchive.net/',
    'Cap Gemini': 'https://www.capgemini.com/fr-fr/?georedirect_none=true',
    'Cresus': "http://www.cresus-france.org/",
    'data leakage': "https://www.kaggle.com/wiki/Leakage",
    "dataframe": "https://pandas.pydata.org/pandas-docs/stable/dsintro.html",
    'dcm': 'https://en.wikipedia.org/wiki/DICOM',
    'ensae_projects': 'https://pypi.org/project/ensae_projects/',
    'ENSAE': "http://www.ensae.fr/",
    'ESUS': "https://www.service-public.fr/professionnels-entreprises/vosdroits/F32275",
    'EY': "https://www.ey.com/fr/fr/home",
    'falcon': "https://falconframework.org/",
    'fatboy': 'https://www.fatboy.com/fr-fr/lamzac',
    "folium": "https://github.com/python-visualization/folium",
    'ijson': "https://pypi.python.org/pypi/ijson",
    'ImageNet': "http://www.image-net.org/",
    'keras': "https://keras.io/",
    'Keras': "https://keras.io/",
    'keyring': "https://pypi.python.org/pypi/keyring",
    'kneighbors': 'https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors.kneighbors',
    'kneighbors_graph': 'https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors.kneighbors_graph',
    'NearestNeighbors': 'https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html',
    'Label Emmaüs': 'https://www.label-emmaus.co/',
    'Latitudes': "http://www.latitudes.cc/",
    'lightmlrestapi': "http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/index.html",
    'Numa': 'https://www.numa.co/',
    'Microdon': "https://www.microdon.org/",
    'Microsoft': 'https://www.microsoft.com/fr-fr',
    "pickle": "https://docs.python.org/3/library/pickle.html",
    "PIL": "https://pillow.readthedocs.io/en/5.3.x/",
    'PIL.Image': "https://pillow.readthedocs.io/en/5.1.x/reference/Image.html",
    'plot_gallery_images': 'http://www.xavierdupre.fr/app/mlinsights/helpsphinx/mlinsights/plotting/gallery.html#mlinsights.plotting.gallery.plot_gallery_images',
    'png': 'https://en.wikipedia.org/wiki/Portable_Network_Graphics',
    'pydicom': 'https://pydicom.github.io/pydicom/stable/getting_started.html',
    'pyensae': 'http://www.xavierdupre.fr/app/pyensae/helpsphinx/',
    'pytorch': 'https://pytorch.org/',
    'radius_neighbors': 'https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors.radius_neighbors',
    'reservoir sampling': 'https://en.wikipedia.org/wiki/Reservoir_sampling',
    'REST': 'https://fr.wikipedia.org/wiki/Representational_state_transfer',
    'REST API': "https://en.wikipedia.org/wiki/Representational_state_transfer",
    'Statup': 'http://statupensae.fr/',
    'Tensorflow': 'https://www.tensorflow.org/',
    'torch': 'https://pytorch.org/',
    'pytorch': 'https://pytorch.org/',
    'urllib3': 'https://urllib3.readthedocs.io/en/latest/',
    "vélib": "https://www.velib-metropole.fr/",
    'VM': 'https://fr.wikipedia.org/wiki/Machine_virtuelle',
    'waitress': "https://docs.pylonsproject.org/projects/waitress/en/latest/",
    'webhtml': 'http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/ensae_teaching_cs/faq/faq_web.html#ensae_teaching_cs.faq.faq_web.webhtml',
    'WSGI': "https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface",
})
