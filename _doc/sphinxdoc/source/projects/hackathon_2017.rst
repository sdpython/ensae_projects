
.. _l-hackathon-2017:

Hackathon Ernst & Young / ENSAE / Genius / Latitudes / Label Emmaüs / 2017
==========================================================================

.. index:: Ernst & Young, ENSAE, Hackathon, Genius, Label Emmaüs, 2017

Le hackathon était proposé et organisé par
`Ernst & Young <http://www.ey.com/fr/fr/home>`_ (sponsor),
`ENSAE <http://www.ensae.fr/ensae/fr/>`_,
`Genius <https://www.facebook.com/geniusensae/>`_,
`Latitudes <http://www.latitudes.cc/>`_,
`Label Emmaüs <https://www.label-emmaus.co/>`_.

.. contents::
    :local:

Les données seront fournies au début de l'événement et doivent être détruites à la fin de l'événement.

Site : `hackathon-geniusensae.fr <http://hackathon-geniusensae.fr/>`_.

.. image:: 2017/hk17.png
    :width: 200

Contexte
--------

`Label Emmaüs <https://www.label-emmaus.co/fr/>`_
propose à la vente en ligne des objets
rénovés ou créés par le mouvement
`Emmaüs <http://emmaus-france.org/>`_.
Son catalogue d'objets
est en croissance régulière. L'ajout d'un objet au catalogue
depuis la réception de sa désignation (images, descriptif, entrepôt)
n'est pas automatisé et prend de plus en plus d'importance.
Chaque vendeur prend plusieurs photos du même objet,
ajoute une description, renseigne d'autres informations
comme sa catégorie.

.. image:: 2017/image2.png
    :width: 100

.. image:: 2017/image3.png
    :width: 150

Pour chaque objet, les informations sont vérifiées, classées, un prix
est fixé puis l'objet est mis en ligne et disponible à la vente.
L'objet est entreposé jusqu'à ce qu'il soit vendu.

.. image:: 2017/image4.png
    :width: 600

La détermination d'un prix comme la rédaction d'une description
ne sont pas toujours simples et il faut un peu de temps et d'expérience
pour traiter rapidement un objet. L'ajout d'un produit prend aujourd'hui
40 minutes jusqu'à la mise en ligne. Beaucoup d'objets restent aussi
très longtemps sur le site avant de trouver acquéreur et l'augmentation
du catalogue nécessite plus d'espace de stockage qui n'est pas toujours
disponible. Trois challenges ont été imaginés pour améliorer la qualité
des données proposées aux futurs acheteurs et optimiser l'espace de
stockage nécessaire.

Trois défis
-----------

Les données sont mis à disposition
des participants uniquement pour la durée du hackathon
et doivent être supprimées à la fin de l'événement
de toutes les ressources utilisées pour répondre
aux défis.

Les données disponibles sont similaires à aux données
d'autres sites de vente en ligne. Il y a trois sources
d'informations : la description des produits vendus
(image, texte, attributs, catégorie, date de mise en ligne, montant),
les ventes elles-mêmes (date de vente, panier),
la composition des paniers (un panier est un acte d'achat
regroupant plusieurs produits).

Les données proposées sont anonymisées. Noms, prénoms, téléphones
sont éliminés, seul est gardé un identifiant crypté. Il n'y a pas de
données de géolocalisation excepté les adresses qui ont été tronquées
(pas de numéro de rue). Cette information a été laissé en clair afin
de pouvoir calculer une estimation de la distance entre l'acheteur
et le vendeur ayant proposé ses produits sur le site.
Les identifiants produits et panier ont été laissés
en clair afin de permettre à *Label Emmaüs* d'exploiter les résultats
trouvés par les participants.

La préparation des données implique une séparation
jeu d'apprentissage, jeu d'évaluation. Ce dernier ne doit pas
comporter la cible à prédire. Les données  réceptionnées ont
moins d'une semaine de retard par rapport au début de l'événement.
Un produit non vendu peut l'être simplement parce qu'il n'est pas resté
assez longtemps sur le site. Intuitivement, il suffit de répartir les
données en apprentissage / évaluation selon l'identifiant produit.
Les paniers introduisent une difficulté, un :epkg:`data leakage`,
car il est possible de déduire la date de vente de tous les
produits d'un même panier à partir d'un seul. De même, si on
veut pouvoir utiliser des données utilisateurs, il faut également
avoir des utilisateurs distincts dans les deux jeux. On
considère l'ensemble des triplets
*(id produits, id personne, id panier)*. Le découpage est fait de telle
sorte qu'aucun de ces identifiants n'apparaissent dans les deux bases.
Il reste un dernier point à propos des données temporelles.
Il devient vite tentant de calculer des moyennes par utilisateur,
par produit sans tenir compte de la date à laquelle cette donnée
est produite. Il en résulte que certaines informations sont utilisées
pour prédire une valeur dans le passé. Ce scénario sera également
vérifié en s'assurant que les modèles produisent les mêmes résultats
des utilisateurs dédoublés mais avec des historiques tronqués.

Challenge deep learning
^^^^^^^^^^^^^^^^^^^^^^^

*bientôt*

Challenge machine learning
^^^^^^^^^^^^^^^^^^^^^^^^^^

*bientôt*

Challenge créatif
^^^^^^^^^^^^^^^^^

*bientôt*

Eléments de code
----------------

**Récupérer des données cryptées**

Pour stocker un mot de passe de façon permanente :

::

    import keyring
    keyring.get_password("hackathon", "labelemmaus", "motdepasse")

Pour décoder tous les fichiers dont l'extension est ``.enc`` :

::

    from pyquickhelper.filehelper import decrypt_stream
    import keyring
    import os

    password = keyring.get_password("hackathon", "labelemmaus")

    encs = os.listdir(".")
    for enc in encs:
        if enc.endswith(".enc"):
            dest = enc[:-4]
            if not os.path.exists(dest):
                print("décrypte", enc)
                decrypt_stream(key=password.encode("ascii"), filename=enc,
                               out_filename=dest, chunksize=2**20)

**Lire de gros fichiers JSON**

Les fichiers JSON proposés pour la compétition contiennent des informations
intéressantes mais ils sont très gros : 1 Go. Il est très difficile
de le regarder depuis un éditeur. Il faut pouvoir le lire en streaming.
C'est ce que fait le module :epkg:`ijson`. La première fonction
l'utilise pour lister les éléments du JSON fourni par :epkg:`Label Emmaüs`.
La documentation fournit un exmple d'utilisation.

.. autosignature:: ensae_projects.hackathon.json_helper.enumerate_json_items

La seconde fonction extrait des champs intéressants. Rien ne vous empêche
de récupérer le code pour extraire d'autres champs.
La documentation fournit un exmple d'utilisation.

.. autosignature:: ensae_projects.hackathon.json_helper.extract_images_from_json_2017

**Manipulation d'images**

* `Search images with deep learning <http://www.xavierdupre.fr/app/mlinsights/helpsphinx/notebooks/search_images.html>`_ :
  le notebook expose comment manipuler des images avec :epkg:`keras` et comment
  utiliser le résultat des couches intermédiaires d'un réseau de neurones profond
  dans le but de recherche des images similaires.

**Cheat Sheets**

.. toctree::
    :maxdepth: 1

    ../notebooks/chsh_graphs
    ../notebooks/chsh_files
    ../notebooks/chsh_dates
    ../notebooks/chsh_pip_install

`Rappel de ce que vous savez déjà mais avez peut-être oublié <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/notebooks/td2_eco_rappels_1a.html>`_

Après la compétition
--------------------

Take Away
^^^^^^^^^

Images
^^^^^^

.. image:: 2017/hk17.png

Vidéo
^^^^^

Agenda
^^^^^^

`Hackathon 2017 <http://www.hackathon-geniusensae.fr/>`_

Lieu : `Numa <https://paris.numa.co/>`_

Vendredi 24 Novembre

* 14h00 - Accueil des participants
* 15h00 - EY, ENSAE, Genius, Latitudes, Label Emmaüs
* 15h45 - Présentation des sujets
* 16h30 - Début du hackathon

Samedi 25 Novembre

* 15h00 - Présentation des résultats
* 17h00 - Remise des prix
* 18h00 - afterwork
