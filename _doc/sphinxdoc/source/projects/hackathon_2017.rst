
.. _l-hackathon-2017:

Hackathon Ernst & Young / ENSAE / Genius / Latitudes / Label Emmaüs / 2017
==========================================================================

.. index:: Ernst & Young, ENSAE, Hackathon, Genius, Label Emmaüs, 2017

Le hackathon était proposé et organisé par
`Ernst & Young <http://www.ey.com/fr/fr/home>`_ (sponsor),
`ENSAE <http://www.ensae.fr/ensae/fr/>`_,
`Genius <https://www.facebook.com/geniusensae/>`_,
`Latitudes <http://www.latitudes.cc/>`_,
:epkg:`Label Emmaüs`.

.. contents::
    :local:

Les données seront fournies au début de l'événement et doivent être détruites à la fin de l'événement.

Site : `hackathon-geniusensae.fr <http://hackathon-geniusensae.fr/>`_.

.. image:: 2017/hk17.png
    :width: 200

Contexte
--------

:epkg:`Label Emmaüs` propose à la vente en ligne des objets
rénovés ou créés par le mouvement `Emmaüs <http://emmaus-france.org/>`_.
Son catalogue d'objets est en croissance régulière. L'ajout de
chaque objet au catalogue depuis la réception de sa désignation
(images, descriptif, entrepôt) est fait indépendamment des autres
objets. Chaque vendeur prend plusieurs photos du même objet,
ajoute une description, renseigne d'autres informations
comme sa catégorie. Au fur et à mesure que le site grossit, la qualité
des informations saisies devient prépondérant afin que
chaque utilisateur puisse facilement trouver l'objet qu'il
recherche.

.. image:: 2017/image2.png
    :width: 100

.. image:: 2017/image3.png
    :width: 150

:epkg:`Label Emmaüs` modèrent les annonces avant leur mise en ligne.
L'objet est entreposé jusqu'à ce qu'il soit vendu.

.. image:: 2017/image4.png
    :width: 600

La détermination d'un prix comme la rédaction d'une description ne sont
pas toujours simples et il faut un peu de temps et d'expérience pour
traiter rapidement un objet. L'ajout d'un produit prend aujourd'hui
40 minutes jusqu'à la mise en ligne. Beaucoup d'objets restent aussi
très longtemps sur le site avant de trouver acquéreur et l'augmentation
du catalogue nécessite plus d'espace de stockage qui n'est pas toujours
disponible. Trois challenges ont été imaginés pour améliorer la qualité
des données proposées aux futurs acheteurs et optimiser
l'espace de stockage nécessaire.

*Pour en savoir plus :* `Label Emmaüs - qui sommes nous ? <https://www.label-emmaus.co/fr/a-propos/qui-sommes-nous/>`_

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
(pas de numéro de rue). Cette information a été laissée en clair afin
de pouvoir calculer une estimation de la distance entre l'acheteur
et le vendeur ayant proposé ses produits sur le site.
Les identifiants produits et panier ont été laissés
en clair afin de permettre à :epkg:`Label Emmaüs` d'exploiter les résultats
trouvés par les participants.

Challenge deep learning
^^^^^^^^^^^^^^^^^^^^^^^

*bientôt*

*Lectures*

L'article n'est pas trop long et pourrait vous donner quelques idées :
`Knowledge Concentration: Learning 100K Object Classifiers in a Single CNN <https://arxiv.org/pdf/1711.07607.pdf>`_.

*Métrique*

C'est un problème de classification multi-label :
chaque produit est associé à une ou plusieurs classes,
le plus souvent imbriquées. Un produit est associé au catégorie
``23946,23958,24038`` ce qui correspond à
*mode, mode homme, chemises*. On pourrait se contenter de ne
prédire que la dernière classe et inférer les deux premières
qui incluent la dernière mais ce n'est pas toujours le cas.
Certains livres sont rangés au rayon jeunesse et au rayon poésie.
Pour prendre en compte ces aspects, on définit une métrique
qui comptabilise le nombre de classes en commun.
On utilise une métriques définies par
`Multi-label classification <https://en.wikipedia.org/wiki/Multi-label_classification>`_
et s'appuyant sur l'indice de `Jaccard <https://en.wikipedia.org/wiki/Jaccard_index>`_.
:math:`C_i=\{c_{i1}, ..., c_{ik_i}\}` est l'ensemble
des classes à prédire pour l'objet *i*, :math:`P_i`
l'ensemble des classes prédite.

.. math::

    E = \frac{1}{n} \sum_{i=1}^n \frac{|C_i \cap P_i|}{|C_i \cup P_i|}

La fonction est implémentée par
`multi_label_jaccard <http://www.xavierdupre.fr/app/lightmlboard/helpsphinx/lightmlboard/metrics/classification.html#lightmlboard.metrics.classification.multi_label_jaccard>`_.

Challenge machine learning
^^^^^^^^^^^^^^^^^^^^^^^^^^

*bientôt*

*Métrique*

C'est un problème de régression mais avec des valeurs infinies.
On aimerait qu'un produit ne reste pas plus de six mois,
c'est pourquoi un produit qui n'a pas été vendu se verra attribuer une
durée de six mois ou 180 jours. Un produit récemment ajouté mais pas encore
vendu sera considéré également comme invendu. Ceci explique l'erreur proposée :

.. math::

    E = \frac{1}{n} \sum_{i=1}^n  \frac{\min \left| Y_i - \min(f(X_i), 180) \right|}{180}

:math:`Y_i \in [0, 180]` est la valeur à prédire, elle est égale à 180
si le produit n'a pas été vendu à la date où est constitué la base de données,
:math:`f(X_i)` est la valeur prédite.
La fonction est implémentée par
`l1_reg_max <http://www.xavierdupre.fr/app/lightmlboard/helpsphinx/lightmlboard/metrics/regression_custom.html#lightmlboard.metrics.regression_custom.l1_reg_max>`_.

Challenge créatif
^^^^^^^^^^^^^^^^^

*bientôt*

Préparation des données
^^^^^^^^^^^^^^^^^^^^^^^

*Cette partie n'est pas essentielle à la compréhension des challenges.
Elle éclaire la façon dont les données ont été préparées pour les
challenges de machine learning.*

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
sorte qu'aucun produit n'apparaît dans les deux bases, et que les
identifiants panier et utilisateurs commun aux deux bases sont réduits.
Ce découpage est réalisé par la fonction
`train_test_connex_split <http://www.xavierdupre.fr/app/pandas_streaming/helpsphinx/pandas_streaming/df/connex_split.html#pandas_streaming.df.connex_split.train_test_connex_split>`_ :

::

    from pandas_streaming.df import train_test_connex_split
    train, test = train_test_connex_split(df, groups=["cart_id","mail","product_id"],
                                          stop_if_bigger=0.05, keep_balance=0.8,
                                          must_groups=["product_id"], test_size=0.2)

Il reste un dernier point à propos des données temporelles.
Il devient vite tentant de calculer des moyennes par utilisateur,
par produit sans tenir compte de la date à laquelle cette donnée
est produite. Il en résulte que certaines informations sont utilisées
pour prédire une valeur dans le passé.

Le fait que ce scénario ne se produit pas pourrait être vérifié
en s'assurant que les modèles produisent les mêmes résultats
avec des produits, des paniers et des utilisateurs dédoublés
mais avec des historiques tronqués. Ceci n'a pas été implémentés
par manque de temps.

Eléments de code
----------------

.. contents::
    :local:

Anti-sèches ou Cheat Sheets
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Essential Cheat Sheets for Machine Learning and Deep Learning Engineers <https://startupsventurecapital.com/essential-cheat-sheets-for-machine-learning-and-deep-learning-researchers-efb6a8ebd2e5>`_
* `PyTorch Cheat Sheet <https://github.com/bfortuner/pytorch-cheatsheet/blob/master/pytorch-cheatsheet.ipynb>`_
* `Keras Cheat Sheet <https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Keras_Cheat_Sheet_Python.pdf>`_

Autres références sur le deep learning

* `Réseaux de neurones et Deep Learning <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/td_2a_mlplus.html#reseaux-de-neurones-et-deep-learning>`_

Récupérer des données cryptées
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Extraire des champs d'un fichier JSON
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le script fonctionne si votre ordinateur a assez de mémoire
pour charger toutes les données. Sinon il faudra passer
au paragraphe suivant pour faire la même chose mais en mode
streaming. Vous trouverez dans les données un exemple des informations
stockées au format JSON pour un seul produit ce qui permettra
d'ajouter facilement d'autres champs au script ci-dessous.

::

    import simplejson
    from dateutil import parser

    with open('full.json') as f:
        js = simplejson.load(f)

    fields = 'product_id|sku|produit|poids|date_created|prix|marchand|merchant_id|statut|stock|categorie|videK|sous-categorie|VideM|VideN|VideO|VideP|VideQ'
    print(fields.replace("|", "\t"))

    for p in js:
        try:
            poids = p['package_weight'].get('kg')
            if poids:
                poids = poids * 1000
            else:
                poids = p['package_weight'].get('g')
        except Exception:
            poids = ''

        created_on = ''
        try:
            created_on = parser.parse(p['created_on']).strftime('%Y-%m-%d')
        except Exception:
            pass

        values = [p['best_offer']['product']['id']),
                  p['best_offer']['sku'],
                  p.get('name',''),
                  str(poids),
                  created_on,
                  str(p['best_offer']['price_with_vat']),
                  p['best_offer']['merchant']['name'],
                  str(p['best_offer']['merchant']['id']),
                  p['best_offer']['status'],
                  str(p['best_offer']['stock']),
                  ]
        values += list(map(lambda x: x['name'], p['application_categories_dict'])
        print("\t".join(values))

Lire de gros fichiers JSON
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Visualiser du JSON
^^^^^^^^^^^^^^^^^^

Le code suivant est extrait du notebook
`Notebook, HTML, SVG, Javascript <http://www.xavierdupre.fr/app/jyquickhelper/helpsphinx/notebooks/notebook_html_svg.html#json>`_.

::

    from jyquickhelper import JSONJS
    with open("product_sample.json", "r") as f:
        js = f.read()
    import json
    rl = json.loads(js)
    JSONJS(rl)

Manipulation d'images et premiers avec le deep learning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Search images with deep learning <http://www.xavierdupre.fr/app/mlinsights/helpsphinx/notebooks/search_images.html>`_ :
  le notebook expose comment manipuler des images avec :epkg:`keras` et comment
  utiliser le résultat des couches intermédiaires d'un réseau de neurones profond
  dans le but de recherche des images similaires.

Cheat Sheets
^^^^^^^^^^^^

N'importe quelle requête sur un moteur de recherche
``cheat sheet + <quelque chose>`` retourne des résultats
intéressants. En voici d'autres...

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
    :width: 500

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
* 16h15 - Installation
* 16h30 - Début du hackathon

Samedi 25 Novembre

* 12h00 - jusque 15h, les mentors vous conseillent sur les présentations,
  soulignent les bonnes idées.
* 15h00 - Mise à disposition du jury du code et des résultats sur GitHub,
  le leaderboard est figé.
* 16h00 - Présentation des résultats - 3 minutes de présentation + 2 minutes de questions
* 17h30 - Délibération du jury
* 18h00 - Cocktail
* 19h00 - After cocktail
