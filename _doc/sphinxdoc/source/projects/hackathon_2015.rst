

.. index:: Microsoft, ENSAE, Hackathon, Croix-Rouge, DataForGood, 2015

Hackathon Microsoft / ENSAE / Croix-Rouge / DataForGood - 2015
==============================================================

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

.. toctree::
    :maxdepth: 2

    hackathon_2015_croix_rouge_other_data


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
    
Un peu plus sur Azure
^^^^^^^^^^^^^^^^^^^^^

* `La bible du hackatonien sur Azure <https://github.com/benjguin/UnlockLuxury/tree/master/doc>`_
* `Provision the Microsoft Data Science Virtual Machine <https://azure.microsoft.com/en-us/documentation/articles/machine-learning-data-science-provision-vm/>`_

