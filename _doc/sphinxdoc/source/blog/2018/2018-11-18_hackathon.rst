
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
    l':epkg:`API REST` accepte l'envoi du plusieurs fichiers et pas seulement deux.
    Deux heures à programmer sans relâche. Il est 11h30, je décide
    de finir les implémentations d'évaluation lors du hackathon.
    A 13h30, je change d'avis et j'ouvre ma valise pour enfourguer
    les cinq coussins glonflables qui ont servi de matelas à
    aux participants ainsi qu'à moi-même.

    14h, je suis à :epkg:`Numa`. Je n'arrive pas à me concentrer pendant 10
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

    16h30 : Je me pose enfin. Jean-Baptiste se bat avec Azure pour démarrer les VM.
    Un compte, une VM. Au-delà, nous atteignons un quota qu'il faut débloquer
    en envoyant un mail, aucune hotline n'a jamais répondu en cinq minutes.
    Autant dire que nous n'essayons même pas. Les adresses mail s'échangent,
    la même carte bleue circule. Espérons que cela suffise.

    17h : Jean-Baptiste termine la liste des :epkg:`VM`, je n'arrive pas à me poser pour
    écrire le script évaluant la prédiction des séries temporelles. Au lieu de ça,
    je passe au démarrage des serveurs d'API REST. Quelques tournées encore.
    Plein de questions.

    18h : Rebelotte. Les groupes discutent stratégie. Qui fait quoi, la direction
    à prendre, les idées à explorer. J'accueille quelques mentors la tête
    dans le guidon. Je dois paraître un peu malpoli. "Faites ce qu'il vous plaît",
    c'est en substance ce que je leur dis.

    19h : Les VM sont prêtes et distribuées, je continue à tourner,
    quelques clés USB s'échangent. Les premiers mentors arrivent.
    J'explique les challenges. Ils se débrouillent pour la suite.
    Je prends un verre de vin puis je retourne à mon clavier, la tête
    courbée sur l'écran.

    20h : Cohue autour du repas. Quelques verres cassés. Les derniers mentors
    arrivent. Une demi-heure plus tard, les élèves reviennent à leurs écrans.
    Un mentor me dit que mon API REST où j'exécute le modèle des élèves pour
    calculer leur performance va probablement planter car je m'appuie sur :epkg:`pickle`
    et que cela ne marche que dans la même configuration. :epkg:`Tensorflow` est encore plus chiant,
    il faut lui nettoyer les sessions. Nous démarrons une VM identique à celle des
    participants. J'attends la première soumission avant de me pencher sur le problème.
    Cela dit mes premiers essais de soumissions n'arriverons que vers 23h.
    C'est compliqué de trouver une demi-heure sans interruption.

    21h : Les questions dures arrivent. J'improvise quelques explications sur
    les séries temporelles. Je partage le fichier des 183 observations
    attendues : Jour, campagne, ratio. J'explique les séries décalées.
    Je debugge des installations de Tensorflow sous mac. Non ça ne marche
    toujours pas sous Python 3.7. La VM d'Azure est toujours sous Python 3.5.
    Pas sûr qu'elle soit mise à jour. Je n'ai pas le temps de vérifier s'il
    y a plusieurs versions installées.

    22h : Les questions vraiment dures : Installer fastai sous Mac. La plus
    dure arrivera vers minuit pour faire tourner un module récupérer sur
    internet et faisant de la détection de texte. Je n'y arriverai pas...
    Je déplie quelques coussins gonflables qui se révèleront très pratiques.
    Antoine me dit qu'il ne restera pas très longtemps, le second aussi
    mais il me l'a répété quasiment jusqu'à la fin.

    23h : Je n'ai pas vraiment le temps de me poser. Je passe de table en table.
    Ils n'ont pas de questions et puis un peu à la manière de Colombo, au moment
    où je tourne les talons, Monsieur je n'arrive pas à faire cela, je suis
    bloqué depuis des heures. Quelques chuchotements me parviennent,
    ils sont censés retenir un voisin de me poser une question jugée trop
    simple et qui pourtant les empêche d'avancer depuis pas mal de temps.
    C'est un des objectifs de l'événement, apprendre à se débrouiller avec
    des données en utilisant toute l'aide à disposition quand bien même cette
    personne aurait séché tous mes cours. L'éducation française... La moindre
    question est synonyme d'ignorance, jamais de curiosité. Et quand bien même,
    elle traduirait l'ignorance, que peut-on faire à part la poser ? Une des
    choses que les élèves me disent une fois le cours passé, je réponds vite
    aux mails, plus vite que la plupart des professeurs.

    00h : Je ne sais plus trop où j'en suis. Je n'ai toujours pas écrit le
    code pour évaluer les soumissions, les premiers groupes essayent. Je me
    suis dit que je m'y mettrai lorsque la première soumission arrivera, ce qui
    fut le cas une heure plus tard. Antoine me dit qu'il va rentrer.
    Le premier est déjà parti. Jean-Baptiste est accaparé comme moi par
    tout un tas de problème liés au deep learning.

    1h : Première tentative de soumission et première requête d'évaluation
    à laquelle je réponds que j'ai besoin d'une heure pour évaluer la
    performance. J'écris le code pendant que Jean-Baptiste et Antoine
    tentent de débugger un Tensorflow récalcitrant. L'espace est petit mais
    à trois mentors pour plus de 80 personnes, on n'a plus le temps de se
    croiser. Le premier temps mort arrivera à 4h du mat. Entre-temps
    j'écris ce foutu bout de code. Je me rends compte que je n'ai toujours
    pas décidé de la métrique à utiliser. J'en code plusieurs. Puis je me
    dis que les participants n'ont pas les données. Il leur sera difficile de
    choisir une direction à partir d'un seul nombre. Je calcule la métrique sur
    différents segments de campagnes en fonction du nombre de dons. Implicitement,
    ils ont une idée de la performance sur les campagnes ayant démarré depuis
    longtemps et sur celle qui viennent de la faire.

    2h : Première soumission évaluée. 100 vont suivre jusque 15h. Pause détente.
    Je repasse parmi les groupes. Enfin, je ne me souviens plus de ce j'ai
    vraiment fait mais c'est probablement ce que j'ai dû faire.
    J'ai un moment de fatigue, j'hésite à dormir maintenant. Deux autres
    mentors sont là. J'ai la tête qui tourne un peu et la nuit courte précédente,
    4h, y est pour beaucoup. Et nous sommes toujours autant sollicités.
    Je refais un tour pour prévenir que je fais un petit somme,
    ça prendra deux heures.

    3h 4h : Je repasse au deep Learning. Le petit coup de fatigue est
    passé. Je grignote un peu. Les questions continuent.

    4h : Je m'octroie finalement une petite pause. J'ai reçu la première
    soumission de deep Learning mais rien ne marche comme prévu. Je choisis
    de somnoler une heure allongé comme je peux recouvert par un sac de couchage.
    J'attends les gens qui mangent parlent sortent, le premier étage a lui
    aussi sombré. Je crois que certains sont partis chez des amis. Il y
    a moins de monde c'est certain. Des 3A me disent qu'elles ont failli ne
    pas revenir. J'avoue que j'ai eu un peu peur à ce moment-là. Jean-Baptiste
    me dit qu'une VM est morte. Il se bat contre Azure pour en démarrer une
    autre. Quand on est fatigué, tout est plus dur.

    5h : Je me relève. J'ai froid, signe que mon corps s'est quelque peu reposé.
    Les mentors n'ont toujours pas dormi. Antoine me dit qu'il ne sait pas
    s'il va rester. Un élève raconte les musées fermés de Barcelone.
    Hilarant. Je ne suis pas le seul à rire. Mais il faut l'avoir écouté
    raconter son voyage... Je termine de coder ce bout de code. Les deux
    soumissions fonctionnent, du moins sur le principe.

    6h : Je passe à l'étage. Ca dort et ça se réveille. Au rez-de-chaussée,
    les coussins gonflables ont du succès. Les soumissions recommencent.
    Je crois que des étudiants reviennent mais les bugs sont revenus me hanter.
    Je suis un peu aveugles à tout ce qui se passe. Je vois un groupe étendu
    sur le :epkg:`fatboy` que j'ai troqué avant de dormir, j'ai échangé leur coussin
    gonflé pour un matelas dégonflé. Ils ont gagné au change, je ne me voyais
    pas agité les deux mains pour remplir d'air ce gouffre rebondissant.

    7h : Un étudiant me pose une question sur les campagnes commencées après
    le début de la période de test. Il souhaite avoir plus d'info. Je lui
    donne la composition des campagnes, la liste des collecteurs, car c'est
    quelque chose de connu au moment de faire la prédiction. Je le partage avec
    tous les participants. Intérieurement, je suis aux anges. J'avais
    volontairement masqué cet aspect pour garder une problématique
    simple très bien transcrite dans la vidéo de l'événement. Je savais que
    cette piste leur permettrait de grappiller quelques points de performance.
    Pour une fois, les quatre astuces que je voyais dans les données ont été
    découvertes par les étudiants. La bataille n'est pas finie. J'ai beaucoup
    d'espoir à ce moment-là et j'ai eu raison. J'ai croisé une élève deux
    semaines plus tard qui me donnait quelques échos... Les participants ont
    beaucoup aimé cette édition qui a été passionnante jusqu'au bout.

    8h : Café. Il est le bienvenu. 5 minutes après, c'est le déluge.
    Tensorflow fait des siennes. Les trois mentors sont autour de la table.
    On ne peut plus bouger. Nous sommes assaillis. Il faut comprendre
    pourquoi Tensorflow plante, récupérer les exceptions. Je passe mon
    temps à réexécuter les codes des élèves. En même temps, je rafraichis
    le leaderboard ML. Le deep Learning patine un peu. Une élève est attendue
    par son groupe pour une discussion stratégique. Elle a disparu pour
    régler un deep problème. Elle est au rez-de-chaussée avec trois
    mentors qui jouent des parties d'échecs en parallèle. C'est fou.

    9h : Je ne vois plus le temps passer. Je suis assis sur la même chaise
    depuis des heures. La première soumission deep est passée. Les groupes
    de machine learning se font la course poursuite sur le leaderboard.
    Le premier a remis un petit cran. Côté deep, Tensorflow fait vraiment
    chier. Le même code plante lorsqu'il est lancé d'une certaine façon
    mais pas d'une autre. Serait-ce dû au fait que le programme est
    importé dynamiquement ? Bizarre quand même. Je recette de ne pas
    avoir implémenté le calcul des perf dans un autre processus. J'ai
    mis une issue sur github. Il va falloir que je lance pas mal de
    trucs à la main. Merde.

    10h : Ca continue. Ca continue. Ca continue. Je ne sais plus ce qu'il
    se passe. J'entends qu'il y a plus de monde mais ma vue se résume
    aux écrans posés devant moi. Le deep fait chier, vraiment chier.
    Pourquoi tout le monde prend Tensorflow ? Ca marche bien sur les machines
    des élèves mais ça voyage très mal. Il parait qu'il faut nettoyer les
    sessions Tensorflow. Ca aide un peu mais ne résout pas tout. Mais il y
    a quoi dans Tensorflow pour que cela soit aussi instable en plus d'être
    très verbeux ? Merde !

    11h :  Je suis toujours assis sur mon tabouret. EY est là je crois,
    Latitudes aussi, je ne suis pas sûr. Les soumissions s'enchaînent et
    je dois mettre à jour le leaderboard manuellement. Le reste du temps
    consiste à debugger les soumissions deep Learning qui retournent des
    résultats différents sur ma machine et sur celles des participants.
    Le cameraman me demande comment ça va... Disons qu'il y a le feu
    partout mais à la différence de l'année dernière, je suis capable de
    calculer des scores. Trois groupes s'affrontent pour le titre de la
    meilleure perf sur le sujet de machine learning. Côté deep, un groupe
    a soumis et a posé la barre assez haut. Je reprends du café et un
    grand verre d'eau.

    12h : Je ne m'en sors pas côté deep. Trois groupes se plaignent de ne pas
    pouvoir soumettre côté machine Learning. Je prends la décision de leur
    donner les images a 13h30. Ils auront une heure pour m'envoyer leur
    prédiction et moi 30 minutes pour calculer toutes leurs scores. Je passe
    chez tous les groupes pour le leur dire. La deadline est à 14h pour les
    groupes de machine Learning qui n'arrivent pas à soumettre via l'API.
    Les fichiers de prédiction doivent être mis sur slack. J'ai une heure devant
    moi, court déjeuner, un rapide bonjour à tout le monde et direction mon
    tabouret pour mettre  jour le leaderboard. Je ne ressens pas la fatigue.
    Je suis confiant. Je suis même joyeux. Je sais ce que je dois faire et
    je sais que je sais le faire. Ecrire cinquante lignes en une heure,
    c'est un sport que j'aime.

    Je m'aperçois en écrivant ces lignes que je n'ai pas beaucoup de souvenirs
    de ce qui se passait autour de moi. Je me souviens d'une discussion avec
    un groupe où j'ai finalement pris la décision de lâcher les images de
    tests à 13h30, d'un autre qui cherchait son général, d'étudiants assis et
    qui peu à peu s'allongent à chacun de mes passages, quelques rires, je passe
    aussi pour leur dire d'éviter de rappeler le sujet dans leur présentation,
    c'est souvent une minute de perdue à dire ce que tout le monde sait. Je ne
    sais plus à combien de question j'ai répondu, j'ai un vague souvenir de
    questions plus techniques que d'habitudes. Python est plutôt bien maîtrisé
    ou alors le partage de connaissance entre les différentes promotions
    fonctionnent bien. Quelques premières années sont venus me voir car un bout
    de code marchait sur tous les portables de l'équipe sauf le leur, souvent des
    macs, celui que je maitrise le moins. Je n'arrive toujours pas à trouver les
    accolades sur le clavier azerty. Je ne comprends pas qu'Apple n'ait pas
    sorti quelque chose de plus élégant depuis.

    13h : Trois groupes font encore la course pour la première place du machine
    learning. Ils soumettent beaucoup. Je me prépare à  calculer le score du deep.
    Je prépare le jeu de test que je zippe et met sur le slack de l'événement.
    Je passe ensuite voir tous les groupes pour m'assurer qu'ils l'ont bien reçu.

    14h : Je calcule la perf des groupes de machine Learning qui n'ont pas réussi
    à soumettre. Il faudra que je simplifie cette partie la prochaine fois. Je partage
    mon script car certaines soumissions retournent des résultats nuls.
    Pandas a quelques côtés cachés parfois subtils surtout en fin de hackathon.
    Ensuite je repasse voir les groupes de deep learning pour voir s'ils arrivent
    à calculer leur perf. Ca a l'air de marcher. Je commence à mettre à jour le
    leaderboard. Quelques soumissions viennent talonner celle qui trône à la
    première place depuis ce matin. J'explique que le taux de 60% de classification
    correspond à une réponse constante.

    15h : Tout est bouclé. J'exhorte le ou les derniers à soumettre maintenant si
    cela n'a pas été fait. Le leaderboard est figé même si je comprends que certains
    ont encore la volonté de le faire bouger. Je propose de commencer les présentations
    à 15h30. Antoine a craqué vers 14h dans un fatboy. Plus de son ni d'image.
    Il s'éveille vers 15h30 comme sorti d'un rêve surpris que le décor ait changé.
    Jean-Baptiste est toujours alerte. Quant à moi, je n'arrête pas d'aller partout
    pour pousser tout le monde vers l'auditoire mais c'est surtout pour ne pas
    m'endormir. Pour la première fois, je fais partie du jury ce que j'avais
    réussi à déléguer jusqu'à présent. Je n'étais pas sûr de rester conscient
    pendant tous les speech. Je redescends pour chercher les derniers retardataires,
    je passe dans les rangs tel un chauffeur de salle tout autant pour me chauffer moi.

    16h : Je prends des notes. Les speech défilent. Les orateurs sont brillants cette
    année. Je me régale sur la phrase : "mon intelligence n'est pas artificielle"
    prononcée par une élève. Il y aura d'autres perles et impertinences, quelques
    commentaires un peu négatifs sur le fait que j'ai coupé les machine virtuelle
    trop tôt. Pour une fois, ils se sont lâchés et c'était bien. J'adore ces
    petites piques.

    17h : Le jury... Il faut décider des prix. J'ai quelques idées mais je ne prends
    pas trop part. Je n'aime pas trop décider des vainqueurs. Je donne deux ou trois
    arguments donne mon approbation. Pour le moment, je savoure. J'ai eu peur tout
    du long, des participants qui arrivent en retard, de ceux qui partent dans la
    nuit, des bugs que je n'avais pas terminé de corriger. Je suis content d'être
    arrivé si loin. Ce hackathon ne ressemble à aucun autre auquel j'ai pu
    participer, c'est bruyant, c'est plein de vie. J'en ai fait un à Londres pour
    Microsoft. Il n'y avait plus que moi comme mentor après 10h du soir.
    Je suis parti à 1h du matin. Je suis revenu à 6h du matin. Je n'avais pas
    arrêté. C'était fou. Les idées les plus intéressantes ne sont pas nécessairement
    celles qu'on voit à la fin sur des slides, ce sont celles qu'on voit naître
    en pleine nuit. Le jury a fini. Les élèves remontent.

    18h : Dernier pot à numa. Champagne. L'ambiance est détendue. Les élèves
    partent assez vite sans doute parce que la plupart habitent maintenant
    Saclay et qu'il reste facilement 1h30 jusqu'à destination. Il faudra
    terminer 1h plus tôt l'année prochaine si on veut étendre ce moment de
    convivialité. Les parisiens partent en dernier. Je distribue quatre fatboy
    pour n'en garder qu'un, celui qui m'avait été offert à Noël l'an dernier et
    que je n'avais pas utilisé jusqu'à présent. Je repars avec ma valise et suit
    les derniers élèves dans un bar pas loin. Je sais que je n'ai que deux heures
    devant moi avant de m'écrouler.

    19h : Direction un bar... Je m'en veux, j'aurais dû faire monter
    les mentors sur scène. Antoine et Jean-Baptiste ont été incroyables.
    Ca n'aurait pas été pareil sans eux. Je me demande pourquoi nous sommes
    tous là, pour défendre une certaine idée de l'école qui nous a diplômés ?
    Pour laisser des souvenirs à plusieurs promotions d'étudiants ?
    L'envie de transmettre... L'envie d'ouvrir une fenêtre dans
    l'école telle que je l'ai connue... Je n'ai jamais vu l'école comme une façon
    d'apprendre un métier utile pour la société. Elle transmet
    un savoir qui confère des pouvoirs magiques.
