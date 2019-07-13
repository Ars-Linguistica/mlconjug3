# -*- coding: utf-8 -*-

"""Utilities."""

import os
import logging


# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except:
        pass

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    basestring
except NameError:
    basestring = str

logger = logging.getLogger(__name__)

level = 'WARNING'
fmt = '\r%(asctime)s%(levelname)8s%(filename)15s %(lineno)4s: %(message)s'
logging.basicConfig(format=fmt, level=level)


def set_save_folder(folder):
    """
    Sets the folder in which conjugation tables will be downloaded and saved.

    :param folder: string.
        Folder path.
    :return: string.
        Folder path.
    """
    if not folder:
        folder = os.path.join(os.path.expanduser("~"), 'Documents', 'mlconjug')
    else:
        folder = os.path.join(folder, 'mlconjug')
    return folder
