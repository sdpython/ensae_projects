"""
@file
@brief Starts an app locally to test it.
"""
from ..datainc import convert_dcm2png as _convert_dcm2png


def dcm2png(folder, dest, fLOG=print):
    """
    Converts all medical images in a folder from format
    :epkg:`dcm` to :epkg:`png`.

    @param      folder      source folder
    @param      dest        destination folder
    @param      fLOG        logging function

    The function uses module :epkg:`pydicom`.
    """
    _convert_dcm2png(folder, dest, fLOG)
