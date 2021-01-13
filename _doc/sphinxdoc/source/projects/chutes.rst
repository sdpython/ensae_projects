Bouts de code en cas de besoin
==============================

.. contents::
    :local:

Récupérer des données cryptées
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour stocker un mot de passe de façon permanente :

::

    from pyquickhelper.loghelper import get_password
    get_password("hackathon", "labelemmaus", "motdepasse")

Pour décoder tous les fichiers dont l'extension est ``.enc`` :

::

    from pyquickhelper.filehelper import decrypt_stream
    from pyquickhelper.loghelper import get_password
    import os

    password = get_password("hackathon", "labelemmaus")

    encs = [f for f in os.listdir(".") if os.path.splitext(f)[-1] == '.enc']
    for enc in encs:
        dest = enc[:-4]
        if not os.path.exists(dest):
            print("décrypte", enc)
            decrypt_stream(key=password.encode("ascii"), filename=enc,
                           out_filename=dest, chunksize=2**20)
