
.. _l-hackathon-2018-code-deep:

Eléments de code pour le challenge 2018
=======================================

.. contents::
    :local:

Extraire un échantillon d'images aléaoires
==========================================

.. code-block:: python

    # -*- coding: utf-8 -*-
    """
    Ce programme sélectionne des fichiers aléatoires dans une
    série de répertoires.
    """
    import os
    import shutil
    import re
    import random

    def random_selection(folder, pattern=".*[.]jpg$", N=1000):
        """
        Sélectionne des fichiers dans un répertoire.

        :param folder: répertoire
        :param N: nombre d'images à sélectionner
        :return: liste fichier
        """
        reg = re.compile(pattern)
        all_files = []
        for root, dirs, files in os.walk(folder):
            for name in files:
                if reg.search(name):
                    all_files.append((root, name))

        sel = random.choices(all_files, k=N)
        return [os.path.join(*_) for _ in sel]

    def copy_files(files, dest):
        """
        Copie des fichiers dans un nouveau répertoire.

        :param files: liste de fichiers
        :param dest: destination
        """
        if not os.path.exists(dest):
            os.makedirs(dest)
        for name in files:
            shutil.copy(name, dest)

    if __name__ == "__main__":
        selection = random_selection('.')
        copy_files(selection, "subset1000")
