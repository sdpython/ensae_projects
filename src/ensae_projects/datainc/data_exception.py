"""
@file
@brief Exception raised when data is not available
"""


class ProjectDataException(Exception):
    """
    Exception raised when data is not available
    """
    pass


class PasswordException(Exception):
    """
    Raised when password is missing
    """
    pass


class FileFormatException(Exception):
    """
    Raised when unable to parse a file
    """
    pass
