"""Utilities."""

import os
import logging


basestring = str

logger = logging.getLogger(__name__)

level = 'WARNING'
fmt = '\r%(asctime)s%(levelname)8s%(filename)15s %(lineno)4s: %(message)s'
logging.basicConfig(format=fmt, level=level)
