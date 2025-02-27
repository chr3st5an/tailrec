"""
MIT License

Copyright (c) 2025 Christian Kreutz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = ["tailrec"]
__version__ = "0.1.3"
__license__ = "MIT"
__author__ = "Christian Kreutz"

from functools import wraps
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)


R = TypeVar('R')
P = ParamSpec('P')


class TailCall(BaseException):
    __slots__ = ("args", "kwds")

    def __init__(self, *args, **kwds):
        super().__init__()
        self.args = args
        self.kwds = kwds


def tailrec(__func: Callable[P, R]) -> Callable[P, R]:
    """Execute a tail recursive function iteratively.

    Notes
    -----
    This decorator does **not** verify if the wrapped function is actually
    tail recursive. This is the responsibility of the user.

    References
    ----------
    https://en.wikipedia.org/wiki/Tail_call

    Examples
    --------
    >>> from tailrec import tailrec
    >>> @tailrec
    >>> def factorial(n: int, accum: int = 1) -> int:
    >>>     if n == 0:
    >>>         return accum
    >>>     else:
    >>>         return factorial(n - 1, accum * n)
    >>> factorial(1_100)
    5343708488092637703...  # No RecursionError
    """
    __recursive__ = False

    @wraps(__func)
    def wrapper(*args: P.args, **kwds: P.kwargs) -> R:
        nonlocal __recursive__

        if __recursive__:
            raise TailCall(*args, **kwds)

        __recursive__ = True

        while True:
            try:
                res = __func(*args, **kwds)
            except TailCall as call:
                args, kwds = call.args, call.kwds  # type: ignore
            else:
                __recursive__ = False
                return res
    return wrapper
