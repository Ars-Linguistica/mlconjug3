"""
Logging utilities for mlconjug3.

This module configures and exposes a module-level logger used across the library.
It ensures consistent formatting and default logging level configuration.
"""

import os
import logging

# NOTE: removed Python 2 compatibility alias (basestring)
# In Python 3, str is sufficient and unified.

logger = logging.getLogger(__name__)

#: Default logging level used by mlconjug3
level = "WARNING"

#: Log format used across the package
fmt = "\r%(asctime)s%(levelname)8s%(filename)15s %(lineno)4s: %(message)s"

logging.basicConfig(format=fmt, level=level)
