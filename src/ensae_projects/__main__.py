# -*- coding: utf-8 -*-
"""
@file
@brief Implements command line ``python -m mathenjeu <command> <args>``.
"""
import sys
from pyquickhelper.cli import cli_main_helper


def main(args, fLOG=print):
    """
    Implements ``python -m ensae_projects <command> <args>``.

    @param      args        command line arguments
    @param      fLOG        logging function
    """
    try:
        from .cli import dcm2png
    except ImportError:
        from ensae_projects.cli import convert_dcm2png  # pylint: disable=W0611

    fcts = dict(dcm2png=dcm2png)
    cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])
