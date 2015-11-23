

.. index:: Croix-Rouge, DataForGood

Data from La Croix-Rouge
========================

* todo
    * compléter la liste des variables intéressantes
    * formules entre les variables
    * comment lier la table ITMMASTER avec les autres (pas de nom de variables)
    
.. contents::
    :local:


Available tables
++++++++++++++++

Following sections do not show the entire schema but the code to get it
assuming you have the necessary credentials to access the data or to
decrypt them (see :ref:`l-cr-pwd`).

ITMMASTER
^^^^^^^^

This table describes items The Red Cross distributes to people in need, their features.


.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("ITMMASTER")
    print(df2rsthtml(df.head(n=2), format='rst'))



SINVOICE
^^^^^^^^

Distribution: what people in need receive from the Red Cross. 

Important fields:

* **BPR**: identifier for a people in need

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE")
    print(df2rsthtml(df.head(n=2), format='rst'))


INVOICE_V
^^^^^^^^^

Table about free workers.

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("SINVOICE_V")
    print(df2rsthtml(df.head(n=2), format='rst'))

stojou
^^^^^^

Daily stocks.

.. runpython::
    :showcode:
    :rst:
    
    from ensae_projects.data.croix_rouge import get_meaning, df2rsthtml
    df = get_meaning("stojou")
    print(df2rsthtml(df.head(n=2), format='rst'))


Quantities in column ``QTYSTU`` can be negative for a donation, positive for a refill.
    

Common columns accross tables
+++++++++++++++++++++++++++++

.. runpython::
    :showcode:
    :rst:
    

    from ensae_projects.data.croix_rouge import merge_schema, df2rsthtml
    df = merge_schema()
    print(df2rsthtml(df.head(n=2), format='rst'))



