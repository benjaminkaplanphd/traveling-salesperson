"""
Entities used throughout the project
"""
from collections import namedtuple
from typing import Tuple


City = namedtuple('City', 'name x y')
Node = Tuple[int, int]
