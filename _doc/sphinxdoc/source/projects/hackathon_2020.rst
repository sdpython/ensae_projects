
.. _l-hackathon-2020:

Hackathon ENSAE / Statup / Cap Gemini - 2020/2021
=================================================

.. index:: Cap Gemini, ENSAE, Hackathon, 2020, 2021

Plusieurs fois reporté à cause de l'épidémie,
il aura lieu en distanciel.
Le hackathon est proposé et organisé par :epkg:`Cap Gemini`
(sponsor), :epkg:`ENSAE`, *Statup*.
Les données seront fournies au début de l'événement
et doivent être détruites à la fin de l'événement.
Site : `Hackathon solidaire Capgemini - ENSAE
<https://www.capgemini.com/fr-fr/evenements/
hackathon-solidaire-capgemini-ensae/>`_.

.. contents::
    :local:

Deux défis
----------

Le cinquième hackathon de l':epkg:`ENSAE` se prépare à ouvrir ses portes
du vendredi 9 au samedi 10 avril 2021. Toujours centré sur le machine Learning,
il proposera deux challenges récoltés proposés par :epkg:`Cap Gemini`.

Challenge machine learning
^^^^^^^^^^^^^^^^^^^^^^^^^^

Proposé par `Too Good To Go <https://toogoodtogo.fr/fr>`_.

Quelques bouts de scripts utiles pour regarder les premiers éléments
sans charger l'intégralité du fichier qui est conséquent (1M de ligne, > 30 colonnes).

::

    # coding: utf-8
    from pandas_streaming.df import StreamingDataFrame

    sdf = StreamingDataFrame.read_csv("train.csv", dtype={'Département': str})
    for df in sdf:
        print(df.head())
        print(df.head().T)
        break

    print(sdf.shape)  # prend du temps car il faut parcourir tout le fichier

Pour stocker la base dans un fichier :epkg:`sqlite`.

::

    import sqlite3
    from pandas_streaming.df import StreamingDataFrame
    
    sdf = StreamingDataFrame.read_csv("df_target.csv", dtype={'Département': str})
    con = sqlite3.connect("tdtd2.db3")
    for i, df in enumerate(sdf):        
        print(i)
        df.to_sql(con=con, if_exists="append", name="tgtd")

    con.close()

Script utilisés pour séparer train/test :

::

    from pandas_streaming.df import StreamingDataFrame
    
    def train_test_iterator(train=True):
        sdf = StreamingDataFrame.read_csv("df_target.csv", dtype={'Département': str})
        
        for df in sdf:
            col = df['date'].apply(lambda s: s[:7]) 
            sel = col < "2020-05"
            if train:
                yield df[sel]
            else:
                yield df[~sel].copy().drop('target', axis=1)
    
    print("test")
    sdf_test = StreamingDataFrame(lambda: train_test_iterator(False))
    sdf_test.to_csv("test.csv", index=False, encoding='utf-8', line_terminator='\n')
    
    print("train")
    sdf_train = StreamingDataFrame(train_test_iterator)
    sdf_train.to_csv("train.csv", index=False, encoding='utf-8', line_terminator='\n')

Challenge Deep Learning
^^^^^^^^^^^^^^^^^^^^^^^

Proposé par `Sea Cleaner <https://www.theseacleaners.org/fr/accueil/>`_.



Après la compétition
--------------------


*Quelques photos...*


Agenda
^^^^^^

Lieu : :epkg:`Cap Gemini`

*Vendredi 9 Avril*

* 14h00

*Samedi 10 Avril*

* 15h30 - Présentation des résultats
