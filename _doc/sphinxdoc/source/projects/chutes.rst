Bouts de code en cas de besoin
==============================

.. contents::
    :local:

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
