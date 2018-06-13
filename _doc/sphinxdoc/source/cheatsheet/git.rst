
.. _l-cheatsheet-git:

Cheat Sheet on Git
==================

.. contents::
    :local:

Add a submodule
+++++++++++++++

::

    git submodule add -b <branch> https://<repo>.git <local path>

Example::

    git submodule add -b investigate https://github.com/sdpython/machinelearning.git cscode/machinelearning

Create a new local branch
+++++++++++++++++++++++++

::

    git checkout -b <new_branch>

Example::

    git checkout -b modif

Create a new remote branch
++++++++++++++++++++++++++

::

    git push -u <remote> <new_branch>

Example::

    git push -u upstream modif

Push modification to remote repository
++++++++++++++++++++++++++++++++++++++

::

    git push

Example::

    git push

Remove a submodule
++++++++++++++++++

::

    git rm <localpath>

The corresponding folder in ``.git/modules/<localpath>`` must be removed too.

Example::

    git rm cscode/machinelearning -f

Update a branch
+++++++++++++++

::

    git pull <origin> <branch>

Example::

    git pull origin master
