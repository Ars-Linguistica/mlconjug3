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
        raise NotImplementedError

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
