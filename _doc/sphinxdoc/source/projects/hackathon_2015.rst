
.. index:: Microsoft, ENSAE, Hackathon, Croix-Rouge, DataForGood, 2015

Hackathon Microsoft / ENSAE / Croix-Rouge / DataForGood - 2015
==============================================================

The hackathon was sponsored by `Microsoft <https://www.microsoft.com/>`_,
the participants were
`ENSAE <http://www.ensae.fr/ensae/>`_'s students
and they worked on data from La `Croix-Rouge <http://www.croix-rouge.fr/>`_.
See `Hackathon <http://variances.eu/?p=146>`_,
`photos <https://www.facebook.com/dsschack/photos/a.1300790849947281.1073741831.1249117758447924/1300793259947040/>`_,
`vidéo <https://www.youtube.com/watch?v=Y1UKAbbExn8>`_.

.. contents::
    :local:

Hackathon
+++++++++

Données et challenge
^^^^^^^^^^^^^^^^^^^^

.. toctree::
    :maxdepth: 2

    hackathon_2015_croix_rouge_schema
    hackathon_2015_croix_rouge_objectives

Autres données
^^^^^^^^^^^^^^

* `dataforgoodfr/croixrouge <https://github.com/dataforgoodfr/croixrouge/tree/master/data>`_
* `Description des tables INSEE <https://github.com/dataforgoodfr/croixrouge/wiki/Description-des-tables-INSEE>`_        		
* Geocoding using Bing Maps : `python-omgeo <https://pypi.python.org/pypi/python-omgeo>`_
* Geocoding using Google Maps : `google-maps-services-python <https://github.com/googlemaps/google-maps-services-python>`_

Documentation
+++++++++++++

.. _l-cr-pwd:

Comment démarrer ?
^^^^^^^^^^^^^^^^^^

Les tables sont grandes, plus de 10 Go, il est quasiment impossible de les charger en mémoire.
Votre ordinateur n'est pas assez puissant mais ce n'est pas un problème,
il suffit de démarrer une machine virtuelle sur Azure, assez puissante,
pour commencer à regarder les données.
Vous pouvez regarder la section suivante pour voir comment faire.

.. toctree::
    :maxdepth: 2

    hackathon_2015_startup

Helpers, notebooks and passwords
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two following notebooks requires access to an Azure Blob Storage.
The credentials to access it can be stored in environment variable ``CRCREDENTIALS``
with following format::

    <blob storage name>**<access key>

Encrypted data available in this module can be accessed setting up
environment variable ``PWDCROIXROUGE`` with with password.

.. toctree::
    :maxdepth: 1

    ../notebooks/upload_donnees
    ../notebooks/database_schemas
    ../notebooks/download_data_azure
    ../notebooks/process_clean_files

Cheat Sheets
^^^^^^^^^^^^

.. toctree::
    :maxdepth: 1

    ../notebooks/chsh_graphs
    ../notebooks/chsh_files
    ../notebooks/chsh_dates
    ../notebooks/chsh_pip_install

Un peu plus sur Azure
^^^^^^^^^^^^^^^^^^^^^

* `La bible du hackatonien sur Azure <https://github.com/benjguin/UnlockLuxury/tree/master/doc>`_
* `Provision the Microsoft Data Science Virtual Machine <https://azure.microsoft.com/en-us/documentation/articles/machine-learning-data-science-provision-vm/>`_
* `SQL DataWarehouse, Azure Machine Learning, Jupyter, Power BI <http://blog.3-4.fr/2015/11/27a/sqldw-azureml-jupyter-powerbi.html>`_
* `Azure PASS <http://aka.ms/azurepassnovembre2015>`_
* `SQL DataWarehouse, Azure Machine Learning, Jupyter, Power BI <http://blog.3-4.fr/2015/11/27a/sqldw-azureml-jupyter-powerbi.html>`_

Fusion des données de la La Croix Rouge avec d'autres
+++++++++++++++++++++++++++++++++++++++++++++++++++++

* `geocoder <https://pypi.python.org/pypi/geocoder>`_
* `dataforgoodfr/croixrouge <https://github.com/dataforgoodfr/croixrouge/tree/master/data>`_
* `Description des tables INSEE <https://github.com/dataforgoodfr/croixrouge/wiki/Description-des-tables-INSEE>`_        		
* Geocoding using Bing Maps : `geopy <https://pypi.python.org/pypi/geopy/>`_ (fonction uniquement en Python 2.7)
