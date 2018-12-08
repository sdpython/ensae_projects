
.. _l-cheatsheet-git:

Cheat Sheet on Git
==================

.. contents::
    :local:

Add a remote
++++++++++++

::

    git remote add <remote_name> <url_repo.git>

Example::

    git remote add upstream_dmlc https://github.com/dmlc/xgboost.git

Add a submodule
+++++++++++++++

::

    git submodule add -b <branch> https://<repo>.git <local path>

Example::

    git submodule add -b branchpy https://github.com/sdpython/machinelearning.git cscode/machinelearning

Checkout a specific file from a remote
++++++++++++++++++++++++++++++++++++++

::

    git checkout [-p|--patch] [<tree-ish>] [--] <pathspec>...

Example::

    git checkout origin/master -- include\xgboost\predictor.h

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

Reset a branch
++++++++++++++

Reset to local branch

::

    git reset --hard <branch>

Reset to a remote branch

::

    git reset --hard <remote>/<branch>

Example:

::

    git reset --hard upstream/master

Reset a submodule
+++++++++++++++++

::

    git submodule foreach git reset --hard

The option ``--recursive`` does it for submodules included
in submodules. Another to do it is to remove the submodule
folder and to type ``git reset --hard`` which removes
every modification made since the last pull.

Update a branch
+++++++++++++++

::

    git pull <remote> <branch>

Example::

    git pull origin master

You can also rebase the repository:

::

    git fetch <remote>
    git rebase <remote>/<banch>

Example::

    git fetch upstream
    git rebase upstream/master

Update a submodule
++++++++++++++++++

::

    git submodule update --remote --merge

Example::

    git submodule update --remote --merge

Update a submodule to the remote branch
+++++++++++++++++++++++++++++++++++++++

::

    git submodule update --init

Example::

    git submodule update --init

Option ``--recursive`` can be added to fetch
submodules inside submodules.
