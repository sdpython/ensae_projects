

.. index:: Croix-Rouge, DataForGood

La Croix-Rouge, Data and Challenges
===================================

Close challenge
+++++++++++++++

Prédiction de la demande


Open challenges
+++++++++++++++

#. **Prédiction de la demande**
    * Gestion des stocks (par départements)
        * source des stocks : `banques alimentaires <http://www.banquealimentaire.org/>`_
        
#. **détection des zones blanches** (peu de bénévoles, demande forte)
    * zones non couvertes par la Croix-Rouge
    * La Croix-Rouge est présent là où il y a des bénévoles
    * croisement des données avec
        * supermarchés
        * autres associations : 
          `Secours Populaire <https://www.secourspopulaire.fr/>`_, 
          `Resto du Coeur <http://www.restosducoeur.org/>`_,
          `Banques Alimentaires <http://www.banquealimentaire.org/>`_
        * taux de bénévolat, population, croiser avec des bases INSEE,
          exemple : `dataforgoodfr/croixrouge <https://github.com/dataforgoodfr/croixrouge/tree/master/data>`_
        * taux de demandes : bénéficiaires du RSA, chômage, quelques tables INSEE :
          `Description des tables INSEE <https://github.com/dataforgoodfr/croixrouge/wiki/Description-des-tables-INSEE>`_
                		
#. **vacances des centres**
    * Les centres ferment (vacances, problèmes de bénévoles
    * détection de ces vacances et prédiction
    * impact sur la distribution des stocks

#. Equilibre du panier
    * Chaque bénéficiaire a droit à une certaine quantité pour une certaine période.
    * A chaque visite, il reçoit un panier qui doit se rapprocher le plus possible d'un 
      panier équilibre (pour des repas équilibrés)
    * Les paniers sont généralement trop chargés en produits gras.
    * Premiers servis = paniers équilibrés, derniers servi = paniers déséquilibrés

#. Qualité des données
    * Données saisies par les bénévoles.
    * Aucun retour pour le moment, pas de réelle incitation 
      à produire des données propres
