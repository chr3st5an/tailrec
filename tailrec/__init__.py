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
__version__ = "0.1.0"
__license__ = "MIT"
__author__ = "Christian Kreutz"


from functools import update_wrapper
from typing import (
    Callable,
    Concatenate,
    Generic,
    ParamSpec,
    TypeVar,
)


R = TypeVar('R')
P = ParamSpec('P')


class _Call(Generic[P]):
    __slots__ = ("args", "kwds")

    def __init__(self, *args: P.args, **kwds: P.kwargs):
        self.args = args
        self.kwds = kwds


class tailrec(Generic[P, R]):
    def __init__(self, __func: Callable[Concatenate[Callable[P, R], P], R]):
        self.__func = __func
        update_wrapper(self, __func)

    def __repr__(self) -> str:
        return repr(self.__func)

    def __call__(self, *args: P.args, **kwds: P.kwargs) -> R:
        res_or_call = self.__func(_Call, *args, **kwds)  # type: ignore

        while isinstance(res_or_call, _Call):
            res_or_call = self.__func(_Call, *res_or_call.args, **res_or_call.kwds)  # type: ignore

        return res_or_call
