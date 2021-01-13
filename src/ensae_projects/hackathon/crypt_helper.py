# -*- coding: utf-8 -*-
"""
@file
@brief Encrypting, decrypting.
"""
import os
import pyquickhelper.loghelper as pl


def _default_name():
    """
    Returns a default username.

    ::

        os.environ.get('USERNAME', os.environ.get('NAME', 'unknown'))
    """
    return os.environ.get('USERNAME', os.environ.get('NAME', 'unknown'))


def get_password(key, username=None):
    """
    Retrieves a password assocatied to *key*.
    Relies on module :epkg:`keyring`.

    @param      key         key
    @param      username    username or ``environ['USERNAME']`` if None
    @return                 password

    .. exref::
        :title: Store and retrieve a password

        Module :epkg:`keyring` can be used to store and retrieve a password.
        It is an easy way to avoid letting clear password in the code.
        To store a password:

        .. runpython::
            :showcode:

            from pyquickhelper.loghelper import set_password
            set_password("system", "username", "password")

        And to retrieve it:

        .. runpython::
            :showcode:

            from pyquickhelper.loghelper import get_password
            pwd = get_password("system", "username")
            print(pwd)
    """
    if username is None:
        username = _default_name()
    return pl.get_password(key, username, ask=False)  # pylint: disable=E1123


def set_password(pwd, key, username=None):
    """
    Stores a password assocatied to *key*.
    Relies on module :epkg:`keyring`.

    @param      pwd         password
    @param      key         key
    @param      username    username or ``environ['USERNAME']`` if None
    @return                 password
    """
    if username is None:
        username = _default_name()
    pl.set_password(key, username, pwd, ask=False)  # pylint: disable=E1123
