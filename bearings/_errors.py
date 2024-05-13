"""

Copyright (c) 2024 c-mcst

License: BSD 3-Clause License. See LICENSE at root of original repository.

Some errors for use in this library.

"""


class IdenticalInputPointError(Exception):
    pass

class ProbableDivergenceError(Exception):
    pass

class AmbiguousIntersectionError(Exception):
    pass

class InfiniteIntersectionError(Exception):
    pass

class AmbiguousBoxError(Exception):
    pass