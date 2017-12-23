# -*- coding: utf-8 -*-
"""
@file
@brief Encrypting, decrypting.
"""
import os
import keyring


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

            import keyring
            keyring.set_password("system", "username", "password")

        And to retrieve it:

        .. runpython::
            :showcode:

            import keyring
            pwd = keyring.get_password("system", "username")
            print(pwd)
    """
    if username is None:
        username = os.environ['USERNAME']
    return keyring.get_password(key, username)


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
        username = os.environ['USERNAME']
    keyring.set_password(key, username, pwd)
