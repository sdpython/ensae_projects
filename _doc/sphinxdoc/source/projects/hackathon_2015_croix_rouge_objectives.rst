

.. index:: Croix-Rouge, DataForGood

La Croix-Rouge, Data and Challenges
===================================

.. contents::
    :local:


.. _l-close-challenge:

Competition
+++++++++++

Prédiction de la demande

* Série temporelle : prédire la demande
* On s'appuie sur les personnes plutôt que les produits car les dons en produits sont limités par les stocks
  disponibles mais si une personne vient, on suppose qu'elle reçoit toujours quelque chose
  et que ce quelque chose devrait être de préférence un panier équilibré correspondant à sa situation
  familiale.
* Scénario concret
    * prédiction du nombre de personnes venant dans chaque départements 
      (nombre de BPR unique par jour et par centre, 
      prédiction par centre difficile pour cause de vacances des centres,
      et les bénévoles ne changent pas de centres : les équipes échangent peu)
    * vérifier que les BPR sont affiliés au même centre 
      (a priori, ce n'est pas possible de vérifier car la base est anonymisée, on le supposera dans ce cas)
    * A finaliser
        * jour *t-7* : La Croix-Rouge provisionne pour la semaine *t* à *t+6* selon la prévision donnée par le modèle
    * Quelques faits
        * Dans les faits, on observe que les centres voisins s'échangent des produits, la prédiction
          par départements devrait rendre cela non significatif.
    


Open directions
+++++++++++++++

#. **Prédiction de la demande**
    * Gestion des stocks (par départements)
        * source des stocks : `banques alimentaires <http://www.banquealimentaire.org/>`_
    * Idée de problématique
        * Voir :ref:`l-close-challenge` 
        * Problématique étendue, faire une prédiction par centre,
          on observe que ce qui est donné, la demande observée n'est pas nécessairement la vraie demande
          car celle-ci est bornée par les stocks. 
          Comment estimer le vrai nombre de demandeur par centre quand ceux-ci sont en vacances.
          Sujet similaire au point 3.
        
#. **Détection des zones blanches** (peu de bénévoles, demande forte)
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
    * Idée de problématique :
        * Comment trier les zones blanches par ordre d'importance ? (prioritiser les zones blanches)
        * Critère de gravité ?
                		
#. **Vacances des centres**
    * Les centres ferment (vacances, problèmes de bénévoles
    * détection de ces vacances et prédiction
    * impact sur la distribution des stocks
    * Idée de problématique
        * Retrouver les vacances des centres (à distinguer des fermetures)
        * Estimer la demande qui n'est pas mesurée
        * Mesurer l'impact sur les centres voisins
        * Distribution des stocks au niveau du département

#. **Equilibre du panier**
    * Chaque bénéficiaire a droit à une certaine quantité pour une certaine période.
    * A chaque visite, il reçoit un panier qui doit se rapprocher le plus possible d'un 
      panier équilibre (pour des repas équilibrés)
    * Les paniers sont généralement trop chargés en produits gras.
    * Premiers servis = paniers équilibrés, derniers servi = paniers déséquilibrés
    * Idée de problématique
        * A stock constant, corriger la distribution des produits pour avoir un panier plus équilibré

#. **Qualité des données**
    * Données saisies par les bénévoles.
    * Aucun retour pour le moment, pas de réelle incitation 
      à produire des données propres
    * Idée de problématique
        * Construire un indicateur qui détermine si tel ou tel centre renseigne mal sa base de données

#. **Tournées du voyageur de commerce**
    * Les produits ne viennent pas tous des mêmes fournisseurs
    * Idée de problématique
        * Comment optimiser une tournée entre plusieurs fournisseurs et plusieurs destinataires ?
