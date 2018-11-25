
.. blogpost::
    :title: Nuit intense au hackathon
    :keywords: ENSAE, EY, Latitudes, BRGM, Microdon
    :date: 2018-11-18
    :categories: hackathon
    :lid: blog-2018-hackathon-rendu

    C'est peu de dire que je suis reparti avec des étoiles
    plein les yeux et pas seulement parce que je n'ai quasiment
    pas dormi durant la nuit du hackathon.
    J'en ai reconnu plusieurs qui à ma grande surprise ont participé
    à trois hackathons, à ma grande surprise parce que je n'imaginais
    pas avant la première édition que cet événement deviendrait un
    périple joyeux et maintenant attendu au point qu'il n'est plus
    besoin de communiquer sur l'événement à l'école pour convaincre
    les élèves de participer. Je ne suis pas le seul à repartir
    du hackathon avec des étoiles, les porteurs de projets
    admiratifs des efforts et des idées produits durant ces
    vingt-quatre heures, du sponsor qui contribue un peu plus
    chaque année, de l'école qui s'investit un peu plus,
    des élèves qui reviennent malgré le côté
    *fabriqué un peu à l'arrache* des défis.

    J'ai plus travaillé sur le côté deep learning cette année.
    Je voulais éviter la difficulté, voire le calvaire de l'année
    précédente. Il ne faut pas trop d'images pour un tel défi.
    J'avais prévu aussi d'implémenter une :epkg:`API REST`
    afin que les participants soumettent leurs solutions de
    façon automatique et que je puisse garder la trace de leur
    travail. L'autre éceuil que je voulais éviter venait de la petite
    taille de la base de données. Si les images de celle-ci étaient
    dévoilées aux équipes, il leur serait alors facile de créer
    les réponses parfaites manuellement. Il fallait que je puisse
    exécuter leur modèle sur une machine. L':epkg:`API REST` répondait
    à ce problème et tout en me permettant de fournir au porteur
    du projet une certaine reproductibilité des résultats.
    Tout ceci m'a tenu occupé jusque jeudi minuit et je
    passai les quatre heures suivantes à regarder les données
    de :epkg:`Microdon` pour définir un challenge qui pourrait
    tenir en haleine les participants jusqu'au bout de la nuit.
    Connaissant la structure des données, j'imaginais trois paliers
    qui induiraient des sauts de performances, l'aspect série temporelle,
    des données qu'il était possible d'agréger, et enfin s'intéresser
    à une prédiction pour des campagnes de collectes de dons
    pour lesquelles il n'existait pas de données pour la simple
    raisons qu'elles avaient commencé après le début de la période de
    test. A minuit, je devais préparer les données, implémenter la
    fonction d'évaluation que je décidais finalement de terminer le
    lendemain après le début de l'événement, et enfin
    vérifier les trois hypothèses que je viens d'évoquer.
    Quelques histogrammes plus loin, il me paraissaient évident qu'il
    fallait prédire des séries temporelles agrégées par semaine,
    les séries quotidiennes montraient quelques pics sur l'année.
    A 3h30, je décidais d'allonger la période de test sur deux mois
    plutôt qu'un mois et demi pour avoir plus de campagnes inconnues.
    A 4h, j'envoyais un mail à un mentor pour lui demander s'il avait le
    temps de jeter un coup d'oeil moins fatigué. Après quelques
    heures de sommeil, je me réveillais avec l'idée qu'il fallait que
    l'API REST accepte l'envoi du plusieurs fichiers et pas seulement deux.
    Deux heures à programmer sans relâche. Il est 11h30, je décide
    de finir les implémentations d'évaluation lors du hackathon.
    A 13h30, je change d'avis et j'ouvre ma valise pour enfourguer
    les cinq coussins glonflables qui ont servi de matelas à
    aux participants ainsi qu'à moi-même.

    14h, je suis à Numa. Je n'arrive pas à me concentrer pendant 10
    minutes et c'est pourtant ce dont j'ai besoin pour écrire de foutu
    code. Je n'ai pas préparer de slides pour les sujets que j'ai
    épurés à l'extrême pour une compréhension rapide.

    14h30 : le premier mentor est là. Jean-Baptiste. Il a organisé
    le hackathon l'année dernière. Je vais un peu mieux.
    Il démarre les machines virtuelles sur Azure. Pas facile.
    Nous luttons contre les limitations, un seul GPU est possible,
    nous utilisons toutes les adresses mails à notre connaissance.
    Une lâchera à 4h du matin...
    
    14h35 : les élèves choisissent quelques tables pour poser leurs
    affaires au premier étage, quelques salles de réunion sont très
    accueillante.

    14h45 : j'abandonne mon clavier. Je modifie une dernière fois
    la page web de l'événement et je lance sa mise à jour.
    J'adore la disposition à la Chéreau. Les speechs commencent bientôt.
    Je n'ai pas encore fini d'implémenter tout ce que je voulais,
    J'anticipe la récupération des images, 4 Go, j'essaye de tout
    copier sur des clés USB que j'ai achetées juste avant de venir.
    Ca prend un temps fou. Mon tour de parler arrive bientôt.
    Le directeur des études mentionne l'arrivée du Python en 2005 à
    l'école, soit un peu avant tout le monde. Je me redresse,
    j'étais là et j'y ai contribué. J'arrête les copies. J'écoute les
    speech. Je passe derrière le rideau pour pousser les derniers arrivés
    vers les places assises. Je monte finalement sur scène, je présente
    deux ou trois images et m'en tiens au strict nécessaire quant 
    à la description des sujets. Je me rappelle l'année dernière,
    j'avais préparé un assez grand speech. Aujourd'hui, pas de transparents,
    jusque trois images pour un challenge, une description sommaire
    pour l'autre. Je voudrais déjà donner quelques astuces,
    deux ou trois petites choses mais je préfère opter pour la 
    simplicité. Le reste se noierait dans l'effervescence.
    
    16h00 : les chaises vibrent, un premier détour vers le goûter et
    c'est parti. Je termine la copie des données un peu stressé car cela
    prend un temps fou, j'aurais préféré faire ça hier. Je fais un tour
    pour m'assurer que tout va bien, les premières questions commencent,
    je ferai deux ou trois tournées avant de pouvoir m'asseoir. A peine
    posé, la première question : *au fait, comment suivre la performance
    sur le sujet de machine learning ?* La réponse évoluera au fil du temps,
    
    
