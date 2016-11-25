

.. index:: Ernst & Young, ENSAE, Hackathon, Croix-Rouge, Crésus, 2016

Hackathon Ernst & Young / ENSAE / Croix-Rouge / Crésus - 2016
=============================================================

.. contents::
    :local:


Les données seront fournies au début de l'événement et doivent être détruites à la fin de l'événement.
Elles sont accompagnés de documents qui permettent d'interpréter certains variables
au regard des activités de chaque association.

Site : `hackathon-geniusensae.fr <http://hackathon-geniusensae.fr/>`_.


Challenge créatif - La Croix-Rouge
++++++++++++++++++++++++++++++++++

La `Croix-Rouge <http://www.croix-rouge.fr/>`_
souhaite comprendre un peu mieux la population de bénévoles
qu'elle emploie.

* Qui est un bénévole fidèle ?
* Qui est un futur responsable bénévole ?
* Comment réagit un bénévole face à des événements de société imprévus (tels que des attentats) ?

L'objectif est de déterminer ce qui motive les bénévoles selon trois axes principaux
afin de proposer le meilleur parcours :

* **L'activité :** dans quelle activité un bénévole s'épanouira-t-il le plus ?
* **L'implication :** quel pourcentage de son temps doit-il y consacrer ?
* **Le niveau de responsabilité :** quel niveau de responsabilité lui conviendrait le mieux ?


Les données incluent une vue globale sur 40 ans et une vue détaillée
pour un secteur de La Croix-Rouge sur les deux dernières années.

*Je veux être bénévole, que me recommandez-vous ?*


Challenge prédictif - Crésus
++++++++++++++++++++++++++++

`Crésus <http://www.cresus-iledefrance.org/>`_ accompagne les personnes en situation de 
surendettement. Les personnes en situation financière difficile commencent par envoyer
un dossier qui précisent les éléments principaux de leur situation. C'est ce que contiennent les bases
*dossier*, *budget*. Un ou plusieurs rendez-vous téléphonique suit pour renseigné les 
tables *agenda* et *crédit*.
Deux colonnes sont utilisées pour qualifier la nature de la situation (diagnostic)
et l'orientation donnée au dossier. Ce sont les deux informations qu'il faut prédire.
Pour ce faire, les tables sont été divisés en apprentissage et test
selon deux ensembles disjoints dans le temps de dossiers.
La base de dossier ne contient pas d'historique.
C'est une vue de la situation au moment où le dossier est orienté.

*Mode d'emploi*

Les différents fichiers sont un dump des différentes tables du système
d'information de l'association. Elles sont liées par des identifiants.
L'identifiant dossier est celui qui permet de lier les données
de la table principale *dossier* aux autres.

La table *dossier* est scindée en deux parties :

* *X* : ensemble des colonnes saisies à la réception d'un dossier
* *Y* : ensemble des informations renseignées manuellement après l'étude d'un dossier.

La partie *Y* contient deux colonnes :

* *nature* : un diagnostique, une raison qui explique le surendettement
* *orientation* : la suite donnée au dossier par l'association *Crésus*

Il faut prédire ces deux colonnes.

    
Autres données
++++++++++++++


* `dataforgoodfr/croixrouge <https://github.com/dataforgoodfr/croixrouge/tree/master/data>`_
* `Description des tables INSEE <https://github.com/dataforgoodfr/croixrouge/wiki/Description-des-tables-INSEE>`_
* `data.gouv.fr <https://www.data.gouv.fr/fr/>`_

    
Cheat Sheets
++++++++++++

.. toctree::
    :maxdepth: 1

    ../notebooks/chsh_graphs
    ../notebooks/chsh_files
    ../notebooks/chsh_dates
    ../notebooks/chsh_pip_install
    
`Rappel de ce que vous savez déjà mais avez peut-être oublié <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/notebooks/td2_eco_rappels_1a.html>`_
    
