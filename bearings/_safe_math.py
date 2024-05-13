"""

Copyright (c) 2024 c-mcst.

License: BSD 3-Clause License. See LICENSE at root of original repository

Some functions to avoid rounding error and modulo weirdness when doing 
great circle math.

"""

import math
from typing import Union

def euclidean_modulo(y: Union[float, int], x: Union[float, int]):
    '''
    Modulo division that follows the sign of the divisor, x
    Needed for intersect formula, because math.fmod() follows the sign of the dividend.
    Args:
        - y: the dividend (number to be divided, aka top of the fraction)
        - x: the divisor (number that the dividend is divided by, aka bottom of the fraction)
    Returns: 
        - the remainder when dividing y by x
    '''
    modulo = y - (x * math.floor(y/x))
    return modulo

# two helpers to avoid rounding error
def asin_safe(x: Union[float, int]):
    """Return the arcsin of x unless abs(x) > 1, then return arcsin of -1 or 1"""
    return math.asin(max(-1,min(x,1)))

def acos_safe(x: Union[float, int]):
    """Return the arccos of x unless abs(x) > 1, then return arccos of -1 or 1"""
    return math.acos(max(-1,min(x,1)))