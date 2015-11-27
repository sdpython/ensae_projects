

.. index:: Croix-Rouge, DataForGood

Données de la Croix-Rouge
=========================

.. contents::
    :local:


Format des fichiers texte
^^^^^^^^^^^^^^^^^^^^^^^^^

* séparateur de colonnes : tab ``\t``
* séparateur de lignes : ``;`` ou ``\n`` (en particulier les fichiers se terminant par ``_.txt``)
* encoding: ``latin-1``
* string: entourées de guillemets ``"``
* les fichiers incluant le suffix 2015 contiennent les mêmes données plus l'année 2015 jusqu'au 24 novembre.

Les fichiers initiaux utilise ``;`` comme séparateur et celui-ci est parfois présent dans les adresses::

    RESIDENCE LE PARC";";1 RUE DU DOC; LAISNEY";" ";"14110";
    
Ce cas n'a pas été bien traité dans les données nettoyées qui vous sont proposées (répertoire ``clean``).

Le paragraphe :ref:`l-sec-com-sch` décrit l'information contenue 
dans la plupart des colonnes de ces tables.



Tables disponibles
++++++++++++++++++

Les paragraphes suivants ne donnent pas les schémas des tables mais
donne seulement un moyen d'y accéder. Les données incluses dans ce module
sont cryptées et nécessitent un mot de passe pour y accéder.
(voir :ref:`l-cr-pwd`).



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

**Remarque**

Cette table a été mal exportée : le nombre de colonne n'est pas fixe
à cause d'une colonne dont le contenu contient parfois des tabulations.


SINVOICE
^^^^^^^^

Cette table décrit les bénéficiaires de la Croix-Rouge et ce qu'il reçoivent (nombre de lignes ~1.4M).
C'est la table utilisée pour comptabiliser le nombre de bénéficiaires par centre et par jour 
(champ ``CREDAT``, ``FCY``, ``BPR``). C'est la table des distributions.
Utiliser ``SINVOICE_.txt`` pour avoir un fichier plat avec un séparateur de ligne ``\n`` et non ``;``,
et ``SINVOICE_.clean.txt`` pour un fichier plat sans guillemets.

*Description of people who receive from the Red Cross.*

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE")
    print(df2rsthtml(df.head(n=2), format='rst'))
    
C'est cette table qui est utilisée pour les séries temporelles du premier défi ::

    SELECT tt.FCY, tt.CREDAT, SUM(tt.nb_foyer) AS nb_foyer_jour FROM (
        SELECT CREDAT, FCY, BPR, COUNT(*) AS nb_foyer
        FROM [SINVOICE_.clean.2015]
        GROUP BY CREDAT, FCY, BPR
    ) AS tt
    GROUP BY tt.FCY, tt.CREDAT
    ORDER BY tt.FCY, tt.CREDAT

Les identifiants ``BPR`` sont uniques excepté pour les personnes anonymes qui reçoivent
le même identifiant. Le nombre de personnes par foyer est environ de 2.5.


SINVOICEV
^^^^^^^^^

Cette table est plus axée sur sur les bénévoles.
Utiliser ``SINVOICEV_.txt`` pour avoir un fichier plat avec un séparateur de ligne ``\n`` et non ``;``,
et ``SINVOICEV_.clean.txt`` pour un fichier plat sans guillemets.

*This table describes the volunteers.*

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE_V")
    print(df2rsthtml(df.head(n=2), format='rst'))




stojou
^^^^^^

Cette table décrit de façon très détaillée les dons et les réceptions de produits.

*This table describes donations and receptions of products.*

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("stojou")
    print(df2rsthtml(df.head(n=2), format='rst'))


Remarques :

* QTYSTU : quantités (négative pour un don, positive pour une réception)


.. _l-sec-com-sch:

Colonnes communes à toutes les tables
+++++++++++++++++++++++++++++++++++++

*Common columns accross tables*

.. runpython::
    :showcode:
    :rst:
    

    from ensae_projects.data.croix_rouge import merge_schema, df2rsthtml
    df = merge_schema()
    print(df2rsthtml(df.head(n=2), format='rst'))



