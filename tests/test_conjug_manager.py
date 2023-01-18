import json
import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import pickle

import pytest

from mlconjug3 import *
