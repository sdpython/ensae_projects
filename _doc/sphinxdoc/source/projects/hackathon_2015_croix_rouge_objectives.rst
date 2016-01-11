

.. index:: Croix-Rouge, DataForGood

La Croix-Rouge, Données et défis
================================

.. contents::
    :local:



Défi performance
++++++++++++++++

Les centres de la Croix-Rouge ouvrent en semaine presque tous les jours. 
Afin de prévoir au mieux la distribution de ses besoins en termes de dons, 
la Croix-Rouge souhaiterait prévoir le nombre de bénéficiaires selon le scénario suivant :

* Le 7 septembre 2014 est un dimanche, un centre de la Croix-Rouge décide de ses jours 
  d'ouverture pour la semaine du 15 au 21 septembre, soit une semaine à l'avance.
* Elle veut estimer le nombre de bénéficiaires pour chaque jour ouvré de cette semaine en ne connaissant que les données jusqu'au 7 septembre.

Ne pas avoir assez de dons à donner est dommageable tant pour les bénéficiaires que pour les bénévoles qui les reçoivent. 
Il faudra minimiser la fonction de coût suivante :

* On note *d* la différence pour le jour *j* : *d(j) = nombre de bénéficiaire(j) - prédiction(j)*
* *Coût(j) = 2 * d(j) si d(j) > 0, -d(j) sinon*
* *Coût = somme Coût(j)*

Evaluation des équipes :

* 20 centres seront fixés à l'avance, il faudra prédire les mois d'octobre et novembre 2015 
* 20 centres seront tirés au hasard, il faudra prédire les mois d'octobre et novembre 2015 (performance prise en compte pour le Jury)


Défi créativité
+++++++++++++++

La Croix-Rouge ne couvre pas tout le territoire français et souhaiterait étendre la zone couverte. 
Mais comment choisir quel quartier ou ville ou département couvrir en premier ? Comment définir un critère 
qui permette de trier ces zones blanches quelles qu'elles soient. Personnes au chômage, 
RSA, autres associations comme les Restaurants du Cœur ou le Secours Populaire, 
à vous de définir le lieu du prochain centre à ouvrir et de proposer un estimateur du nombre de personnes qui y viendront ? 

Les prédictions seront invérifiables, à vous de nous montrer qu'on peut vous croire.


