
.. _l-hackathon-2018:

Hackathon ENSAE / BRGM / Microdon / Latitudes / Genius / Ernst & Young - 2018
=============================================================================

.. index:: Ernst & Young, ENSAE, Hackathon, Genius, Microdon, BRGM, 2017

Le hackathon est proposé et organisé par
`Ernst & Young <http://www.ey.com/fr/fr/home>`_ (sponsor),
`ENSAE <http://www.ensae.fr/ensae/fr/>`_,
`Genius <https://www.facebook.com/geniusensae/>`_,
`Latitudes <http://www.latitudes.cc/>`_,
:epkg:`BRGM`, :epkg:`Microdon`.
Les données seront fournies au début de l'événement
et doivent être détruites à la fin de l'événement.
Site : `hackathon-geniusensae.fr <http://hackathon-geniusensae.fr/>`_.

.. contents::
    :local:

.. image:: 2018/visuel_affiche.png
    :height: 300

Deux défis
----------

Le quatrième hackathon de l':epkg:`ENSAE` se prépare à ouvrir ses portes
du vendredi 16 au samedi 17. Toujours centré sur le machine Learning,
il proposera deux challenges récoltés par l'association Latitudes -
:epkg:`Latitudes` participe à la transformation de l'enseignement des ingénieurs
et des développeurs, afin de favoriser leur engagement durable sur des
projets qui œuvrent pour l'intérêt général -. Il aura lieu chez Numa, et
comme l'année dernière, il est sponsorisé par :epkg:`EY`.

Le premier défi, orienté deep Learning, s'intéressera à la
reconnaissance de dommages dans des images liées à des inondations
ou des séismes. Ce challenge est proposé par le
:epkg:`BRGM` - Le Bureau de Recherches Géologiques et Minières est l'établissement
public de référence dans les applications des sciences de la Terre pour
gérer les ressources et les risques du sol et du sous-sol -.
Le second challenge est préparé par :epkg:`Microdon` - une start-up agréée
:epkg:`ESUS` et certifiée :epkg:`B-Corp` qui propose aux entreprises soucieuses de
leur Responsabilité sociétale des solutions innovantes pour faciliter
l’engagement solidaire en entreprise -. Il s'attaquera a un problème de
prédiction de séries temporelles pas si éloigné d'ailleurs d'un des
sujets du premier hackathon organisé en 2015. Le hackathon innove
cette année pour faciliter le passage de témoin entre les participants
et les associations. Il est prévu que les prédictions des modèles
soient accessibles via une :epkg:`API REST` afin de permettre aux porteurs de
projets de s'approprier plus facilement le travail des étudiants.

Challenge deep learning
^^^^^^^^^^^^^^^^^^^^^^^

La construction d'un défi n'a pas été simple pour ce challenge.
Une vue d'ensemble des images montre que les photos partagées
sur twitter illustrent des inondations sérieuses, des voitures sous
l'eau, des bateaux dans les rues. Il y a peu de photos d'intérieures
dévastés. Le problème est plus flagrant pour les séismes ou peu de
gens prennent des photos au regard du nombre de gens
qui les propagent. Cela tient sans doute à la soudaineté
de la catastrophe. Les personnes sont surprises et plongées
dans l'urgence alors qu'une inondation monte lentement et laisse
le temps de prendre des photos du danger. On part également du principe
que les gens prendront d'abord une photo d'une rivière qui monte,
puis d'une voiture ou d'une rue. Partant de ce principe, la gravité
de l'inondation est indiqué par ce que contient la photo :
une rivière ou un élément de la ville, rue ou voiture.
Le challenge doit répondre à deux questions à partir d'une image :

**L'image concerne-t-elle une inondation ou un séisme ?**

.. image:: 2018/imp.jpg
    :width: 200

La base d'images sur tweeter regroupe de nombreuses images
d'inondations ou de séimes, des cartes. A cela ont été ajoutées
des images de la base :epkg:`ImageNet` pour avoir des images
de rues non inondées assez rares dans la base récoltées par
le :epkg:`BRGM`. Des images ont été récupérées depuis l'url
suivant : `ImageNet/street <http://www.image-net.org/search?q=street>`_.
Il n'est pas interdit d'en ajouter d'autres surtout
pour obtenir des images sans inondations ou séismes qui n'ont pas
été ciblées par la méthode de sélection.
Le jeu de données fourni pour le hackathon contient :

* Les images initiales extraites de tweeter.
* Les images sans doublons extraites par une méthode statistiques.
* Des images extraites de :ref:`ImageNet` et de :ref:`Bing`
* Quelques images annotées.

La difficulté de ce challenge vient du fait que peu d'images sont
labellisées et qu'il faudra probablement augmenter la base
avec des images venant d'internet pour contrebalancer la surreprésentation
des images d'inondations.

On pourra regarder si l'image contient une voiture, une rue,
une rivière et s'en servir pour classer les images.
La base d'évaluation contient environ 200 images qu'il faudra classer
avec précision. Il y a quelques **pièges** :

.. list-table::
    :header-rows: 0
    :widths: 5 5 5 5

    * - .. image:: 2018/imn1.jpg
            :width: 150
      - .. image:: 2018/imn2.jpg
            :width: 150
      - .. image:: 2018/imn3.jpg
            :width: 150
      - .. image:: 2018/imn4.jpg
            :width: 150

La moitié des images sont dites indésirables, elles représentent
des dessins, des cartes ou des photos d'écrans.

Challenge machine learning
^^^^^^^^^^^^^^^^^^^^^^^^^^

Microdon reçoit des dons de nombreux points de collecte
pour les redistribuer ensuite à de nombreuses associations.
La base de données contient plus d'un million de lignes anonymisées
pour des dons agrégées par jour. Les huit dernières semaines vous sont
inconnues mais il faudra prédire les sommes agrégées par semaine
pour chaque campagne pour ces huit semaines manquantes, soit environ
200 valeurs. Il faut prédire le **taux de participation** d'une
campagne agrégrée par semaine.

.. image:: 2018/micro.png

Le numéro de la semaine est déterminé par la fonction
`dt.week <https://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.Series.dt.week.html>`_.

Eléments de code
----------------

.. toctree::

    hackathon_2018_api_rest
    hackathon_2018_code_deep

Après la compétition
--------------------

Ce fut une belle bataille. Je n'avais pas tout-à-fait
automatisé le leaderboard que je devais mettre à jour
manuellement. Je n'ai pas pu quitter mon ordinateur
entre 8h et 15h où je fus presque forcé de dire que je
n'admettais plus aucune soumission.

.. list-table::
    :header-rows: 0
    :widths: 10 10

    * - .. image:: 2018/nb2018.png
            :width: 400
      - .. image:: 2018/perf2018.png
            :width: 400

Les données ont gardé quelques secrets jusqu'à la fin
de l'événement qui ont été dévoilés par de brillants orateurs
lors des présentations.
Vers 8h du matin, après quelques pains aux chocolat et plusieurs
tasses de cafés, les équipes ont commencé à s'intéresser
aux campagnes qui n'avaient pas débuté à la date du 15 septembre
qui constituaient le premier jour de la base d'évaluation choisie
pour comparer les résultats. La bataille pour la première place
s'est quelque peu intensifiée. Le challenge deep learning n'est
pas resté sur la touche. J'ai découvert la galère que cela
peut être de faire tourner un modèle *tensorflow* sur une machine
alors qu'il a été appris sur une autre. Si le deep learning
paraît la rolls des modèles, il ne roule pas sur toutes les routes
sans changer de pneus. Je n'aurais jamais pu survivre à tous les
problèmes que les participants ont évoqués sans l'aide incroyable
des mentors et amis qui m'ont accompagné toute la nuit.
Il est toujours difficile d'anticiper les problèmes et comme l'année
dernière, je suis venu avec quelques nuits courtes dans les jambes
et quelques bouts de code encore à coder pour évaluer les équipes.
Vous pourrez lire un récit de cet épique marathon dans cet
article de blog : :ref:`blog-2018-hackathon-rendu`.

J'apprécie toujours autant l'ambience de ces deux jours où
le fait que tous soient de la même école contribue pour beaucoup
à la convivialité. Les temps morts sont très rares, c'est un peu plus
calme entre quatre et cinq heures du matin mais en fait je ne suis pas
sûr car c'est souvent le moment que je choisis pour m'allonger
une heure pour ne pas m'écrouler à 10h du matin plutôt qu'à 10h du soir.
Les bruits paraissent plus lointains.

Encore une fois, j'ai été surpris par l'abnégation et l'inventivité
des participants.

Résultats
---------

La prédiction sur le challenge machine learning a atteint 90%
de corrélation entre la série attendue et la série prédite
pour le meilleur des groupes. Ils ont distingué les campagnes qui
avaient déjà commencé de celles qui commençaient après le debut
de la période de test et ont proposé deux modèles.

Le challenge deep learning a tourné autour des 80% de performance.
Cela peut sembler peu mais si on utilise ce modèle pour construire
un système d'alerte. Malgré le nombre de faux positifs, il est à
peu près sûr que ce nombre augmentera rapidement en cas de catastrophe.
C'est comme si d'une période normale avec 20% d'images considérées
comme des inondations, on passait tout à coup à 40%. Dans le lot,
la moitié sont toujours détecté par erreur, quant aux autres, elles
suffiront à retenir l'attention en temps réel.

Communication
-------------

Photos
^^^^^^

.. image:: 2018/EY002.jpg
    :width: 300
.. image:: 2018/EY012.jpg
    :width: 300
.. image:: 2018/EY017.jpg
    :width: 300
.. image:: 2018/EY019.jpg
    :width: 300
.. image:: 2018/EY023.jpg
    :width: 300
.. image:: 2018/EY027.jpg
    :width: 300
.. image:: 2018/EY032.jpg
    :width: 300
.. image:: 2018/EY034.jpg
    :width: 300
.. image:: 2018/EY053.jpg
    :width: 300
.. image:: 2018/EY057.jpg
    :width: 300
.. image:: 2018/EY095.jpg
    :width: 300
.. image:: 2018/EY099.jpg
    :width: 300
.. image:: 2018/EY112.jpg
    :width: 300
.. image:: 2018/EY141.jpg
    :width: 300
.. image:: 2018/EY170.jpg
    :width: 300

Vidéo
^^^^^

Agenda
^^^^^^

Lieu : `Numa <https://paris.numa.co/>`_

*Vendredi 16 Novembre*

* 14h00 - Accueil des participants
* 15h00 - EY, ENSAE, Genius, Latitudes, Microdon, BRGM, Numa
* 15h45 - Présentation des sujets
* 16h15 - Début du hackathon

*Samedi 17 Novembre*

* 15h45 - Présentation des résultats - 4 minutes de présentation + 1 minute de questions
* 17h30 - Délibération du jury
* 18h00 - Cocktail
* 19h00 - After cocktail

Le lien vers le site de l'événement,
`Hackathon 2018 <http://www.hackathon-geniusensae.fr/>`_,
valide uniquement un mois dans l'année.
