# -*- coding: utf-8 -*-

"""Utilities."""

import os
import re
from stem import Signal
from stem.control import Controller
from urllib3.contrib.socks import SOCKSProxyManager
import certifi

import gevent.monkey
import socket

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except:
        raise NotImplementedError

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    basestring
except NameError:
    basestring = str


def set_save_folder(folder):
    """
    Sets the folder in which lyrics will be downloaded and saved.

    :param folder: string.
        Folder path.
    :return: string.
        Folder path.
    """
    if not folder:
        folder = os.path.join(os.path.expanduser("~"), 'Documents', 'LyricsMaster')
    else:
        folder = os.path.join(folder, 'LyricsMaster')
    return folder
