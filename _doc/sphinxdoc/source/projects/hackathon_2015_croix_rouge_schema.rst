

.. index:: Croix-Rouge, DataForGood

Données de la Croix-Rouge
=========================

.. contents::
    :local:


Tables disponibles
++++++++++++++++++

Les paragraphes suivants ne donnent pas les schémas des tables mais
donne seulement un moyen d'y accéder. Les données incluses dans ce module
sont cryptées et nécessitent un mot de passe pour y accéder.
(voir :ref:`l-cr-pwd`).


**Format**

* séparateur de colonnes : tab ``\t``
* séparateur de lignes : ``;`` ou ``\n`` (en particulier les fichiers se terminant par ``_.txt``)
* encoding: ``latin-1``
* string: entourées de guillemets ``"``


ITMMASTER
^^^^^^^^^

Cette table décrit les produits distribués par la Croix-Rouge.

*This table describes items The Red Cross distributes to people in need, their features.*


.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("ITMMASTER")
    print(df2rsthtml(df.head(n=2), format='rst'))



SINVOICE
^^^^^^^^

Cette table décrit les bénéficiaires de la Croix-Rouge (nmbre de lignes ~1.4M).
Utiliser ``SINVOICE_.txt`` pour avoir un fichier plat avec un séparateur de ligne ``\n`` et non ``;``.

*Description of people who receive from the Red Cross. *

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE")
    print(df2rsthtml(df.head(n=2), format='rst'))

Variables importantes :

* **BPR**: identifiant des bénéficiaires


INVOICE_V
^^^^^^^^^

Cette table décrit les bénévoles.

*This table describes the volunteers.*

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE_V")
    print(df2rsthtml(df.head(n=2), format='rst'))
    
Variables importantes :



stojou
^^^^^^

Cette table décrit les dons et les réceptions de produits.

*This table describes donations and receptions of products.*

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("stojou")
    print(df2rsthtml(df.head(n=2), format='rst'))


Variables importantes :

* QTYSTU : quantités (négative pour un don, positive pour une réception)

    

Colonnes communes à toutes les tables
+++++++++++++++++++++++++++++++++++++

*Common columns accross tables*

.. runpython::
    :showcode:
    :rst:
    

    from ensae_projects.data.croix_rouge import merge_schema, df2rsthtml
    df = merge_schema()
    print(df2rsthtml(df.head(n=2), format='rst'))



