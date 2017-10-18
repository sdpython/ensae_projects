"""
@file
@brief Helpers around credentials.
"""
import warnings


def set_password(k1, k2, value):
    """
    Stores a password with `keyring <http://pythonhosted.org/keyring/>`_.

    @param      k1      first key
    @param      k2      second key
    @param      value   value

    .. faqref::
        :title: How to avoid entering the credentials everytime?

        Using clear credentials in a program file or in a notebook
        is dangerous. You should do that. However, it is annoying
        to type his password every time it is required.
        The solution is to store it with `keyring <http://pythonhosted.org/keyring/>`_.
        You need to execute only once:

        ::

            keyring.set_password("k1", "k2", "value")

        And you can retrieve the password anytime
        not necessarily in the same program:

        ::

            keyring.set_password("k1", "k2", "value")
    """
    if not isinstance(k1, str):
        raise TypeError("k1 must be a string.")
    if not isinstance(k2, str):
        raise TypeError("k1 must be a string.")
    if not isinstance(value, str):
        raise TypeError("value must be a string.")
    if len(value.strip()) == 0:
        raise ValueError("value is empty")
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        import keyring
    keyring.set_password(k1, k2, value)


def get_password(k1, k2):
    """
    Retrieves a password with `keyring <http://pythonhosted.org/keyring/>`_.

    @param      k1      first key
    @param      k2      second key
    @param      value   value
    """
    if not isinstance(k1, str):
        raise TypeError("k1 must be a string.")
    if not isinstance(k2, str):
        raise TypeError("k1 must be a string.")
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        import keyring
    value = keyring.get_password(k1, k2)
    if value is None:
        raise ValueError(
            "No secret value stored for k1={0} k2={1}".format(k1, k2))
    return value
