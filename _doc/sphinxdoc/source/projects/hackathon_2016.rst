
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
**Il ne faut pas utiliser la colonne etat** qui est renseignée
manuellement après *nature* et *orientation*.

Compétition
+++++++++++

La compétition est accessible sur codalab :
`Hackathon ENSAE - EY - Challenge Crésus - 1.5 <https://competitions.codalab.org/competitions/15490>`_.
C'est un problème de classification **multi-classes**.

* `données du challenge <https://github.com/sdpython/ensae_projects/blob/master/_doc/competitions/2016_ENSAE_hackathon/competition/data_cresus.zip>`_

Les réponses doivent être données dans le même ordre que les lignes de la table
``tbl_dossier.test.X.txt`` dans un fichier texte sans en-tête **answer.txt**.
Soumettre une solution consiste à envoyer à fichier **answer.zip** qui contient un
fichier **answer.txt** au format suivant :

::

    4.0  endettement  0.9144635693307518  0.7446166038448464
    2.0  endettement  0.9058230082126213  0.5672372371792938
    1.0  credits renouvelables recurrents  0.963522847810654  0.4201954811133858
    2.0  difficultes de gestion  0.6700924948192609  0.5024330719247078
    5.0  microcredit social  0.33637962518435127  0.5765688167949408
    1.0  impayes  0.2746943724528652  0.16503183971336655
    5.0  microcredit personnel  0.695436159178639  0.7331150383369753

Avec quatre colonnes :

#. prédiction pour l'**orientation**
#. prédiction la **nature**
#. **score orientation** pour la prédiction de l'orientation
#. **score nature** pour la prédiction de la nature

Un exemple de soumission est disponible (réponse aléatoire)

#. `answer.txt <https://github.com/sdpython/ensae_projects/blob/master/_doc/competitions/2016_ENSAE_hackathon/competition/answer.txt>`_
#. `answer.zip <https://github.com/sdpython/ensae_projects/blob/master/_doc/competitions/2016_ENSAE_hackathon/competition/answer.zip>`_

Les métriques produites pour chaque colonne :

* **ERR - taux d'erreur** : c'est la proportion de mauvaises prédictions,
  la classe prédite n'est pas la classe attendue.
* **AUC - aire sous la courbe ROC** : ce chiffre correspond à la probabilité
  pour le score d'une bonne prédiction d'être supérieur au score d'une mauvaise
  prédiction - `Courbe ROC <http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/c_metric/roc.html>`_.

Une bonne *AUC* indique que le score de la prédiction est fiable.
Autrement dit, même si le taux d'erreur est élevé, cela signifie que celui qui utilise
le modèle de prédiction peut plus facilement croire la prédiction quand celle-ci est élevée.
Cette métrique a été choisie pour permettre à l'utilisateur d'automatiser
une partie du traitement avec fiabilité et de continuer à gérer les autres
dossiers manuellement lorsque la prédiction n'est pas assez fiable.
La fonction de calcul *AUC*
est implémentée : :func:`AUC_multi <ensae_projects.ml.competitions.AUC_multi>`
et le fichier d'évaluation fonctionne en Python 2 ou 3 :
`evaluate.py <https://github.com/sdpython/ensae_projects/blob/master/_doc/competitions/2016_ENSAE_hackathon/competition/program/evaluate.py>`_.

Résultats du challenge prédiction
+++++++++++++++++++++++++++++++++

+-----------+-----------------+-----------------+------------+------------+
| Team Name | orientation_ERR | orientation_AUC | nature_ERR | nature_AUC |
+-----------+-----------------+-----------------+------------+------------+
| 3         | 0.7503          | 0.7125          | 0.8707     | 0.4744     |
+-----------+-----------------+-----------------+------------+------------+
| 7         | 0.5272          | 0.6403          | 0.6936     | 0.4902     |
+-----------+-----------------+-----------------+------------+------------+
| 7         | 0.5245          | 0.6750          | 0.9270     | 0.5339     |
+-----------+-----------------+-----------------+------------+------------+
| 5         | 0.5202          | 0.6349          | 0.7084     | 0.5330     |
+-----------+-----------------+-----------------+------------+------------+
| 10        | 0.5146          | 0.6109          | 0.7138     | 0.5459     |
+-----------+-----------------+-----------------+------------+------------+
| 11        | 0.4797          | 0.6652          | 0.7282     | 0.5000     |
+-----------+-----------------+-----------------+------------+------------+
| 1         | 0.4058          | 0.6499          | 0.6455     | 0.5544     |
+-----------+-----------------+-----------------+------------+------------+

La compétation est terminée. Les prédictions attendues sont disponibles
zippées : `reference.zip <https://github.com/sdpython/ensae_projects/blob/master/_doc/competitions/2016_ENSAE_hackathon/competition/reference.zip>`_.

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

Retour sur la compétition
+++++++++++++++++++++++++

**événements**

La qualité des données a un gros impact sur la performance et
on découvre les données trop souvent sous la forme de tableau de bord
alors que ceux-ci sont la conséquence d'une succession d'événements.

Si un système d'information ne conserve que l'état d'une situation,
d'une association, il ne représente que le présent, perd toute notion
d'historique et met côte à côte des informations qui n'ont pas
été renseignées à la même date.

C'est pourquoi il est beaucoup plus intéressant de construire un système
qui enregistre des événements, des mises à jour. Il est facile de reconstruire l'état
du système à partir de cette séquence. Cela permet pour un datascientist
de comprendre l'évolution des données, de déterminer quelles données étaient
disponibles à chaque instant surtout si elles ont servi de base
à une décision. Ce procédé notamment de repérer qu'une variable est renseignée
après une autre et qu'elle en dépend.

**id_dossier**

Certains participants ont noté que la variable
*id_dossier* avait un impact positif sur la qualité de la prédiction.
Faut-il s'en passer sachant qu'elle n'a pas de sens particulier ?
Dans l'idéal, oui ! Mais avant de prendre une décision hâtive,
il faut s'interroger sur le fait que cette variable ait un impact.
Tout d'abord, le numéro de dossier est croissant. Il est donc plus ou moins
corrélé avec la date à laquelle le dossier est ouvert.
On peut remplacer *id_dossier* par la date et mesurer la
différence de prédiction. Toutefois, on peut se demander pourquoi
la date aurait un impact sur la prédiction. Cela signifie probablement
que la distribution de la variable *orientation* évolue avec le temps
et que la base de test n'est probablement pas tout à fait homogène
avec la base d'apprentissage puisque le découpage a eu lieu par rapport au temps.
On peut utiliser une astuce pour vérifier :
`Les bases de train et test sont-elles homogènes ? <http://www.xavierdupre.fr/app/jupytalk/helpsphinx/2016/ensae201611.html#faq>`_.

**données aberrantes**

Il n'existe pas toujours de mode d'emploi. Lorsqu'on voit une
valeur *2010-2110* avec une colonne qui porte la mention *début-fin*,
cela signifie sans doute que le début est bien 2010 mais que la fin n'est
pas déterminée. Mais comme le système d'information la demande,
la personne qui a renseigné l'information en donne une plus ou moins aberrante.
Plus les gens se servent d'une base de données, meilleure elle est.
