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
__version__ = "0.1.5"
__license__ = "MIT"
__author__ = "Christian Kreutz"

from types import FrameType, TracebackType
from collections import UserDict
from functools import wraps
from typing import (
    Any,
    Callable,
    cast,
    ParamSpec,
    TypeVar
)
import dis
import sys


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
    if not hasattr(__func, "__code__"):
        raise TypeError("Expecting a function as argument.")

    # The bytecode offsets of all return instructions present
    # in the given function
    returns = {
        inst.offset: True for inst in dis.Bytecode(__func.__code__)
                            if inst.opname == "RETURN_VALUE"
    }

    @wraps(__func)
    def wrapper(*args: P.args, **kwds: P.kwargs) -> R:
        caller = sys._getframe()

        try:
            # Detecting recursive call
            while caller := caller.f_back:
                if caller.f_code is __func.__code__:
                    raise TailCall(*args, **kwds)
        finally:
            del caller

        # Weather the wrapper should return a final value.
        # False, if there appears a recursive call in the
        # wrapped function without a return statement.
        __return__ = True

        while True:
            try:
                res = __func(*args, **kwds)
            except TailCall as call:
                tb = cast(TracebackType, call.__traceback__)
                caller = cast(TracebackType, tb.tb_next)

                args, kwds = call.args, call.kwds  # type: ignore
                __return__ &= returns.get(caller.tb_lasti + 2, False)

                del call, caller, tb
            else:
                return res if __return__ else None  # type: ignore

    return wrapper
