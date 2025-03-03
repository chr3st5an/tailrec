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

from functools import wraps
from typing import (
    Callable,
    ParamSpec,
    TypeVar
)

from tailrec import tailrec


P = ParamSpec('P')
R = TypeVar('R')


def identity(__func: Callable[P, R]) -> Callable[P, R]:
    """Decorator which simply executes the given function"""
    @wraps(__func)
    def wrapper(*args: P.args, **kwds: P.kwargs) -> R:
        return __func(*args, **kwds)
    return wrapper


@tailrec
def factorial(n: int, accum: int = 1) -> int:
    if n > 0:
        return factorial(n - 1, accum * n)
    else:
        return accum


def _factorial(n: int):
    product = 1

    while n > 0:
        product *= n
        n -= 1

    return product


@tailrec
def ping_pong(n: int) -> None | str:
    if n <= 1:
        return "pong"

    if 1 < n < 100:
        return ping_pong(n % 2)

    # No return
    ping_pong(n - 10)


def test_factorial():
    assert hasattr(factorial, "__name__")
    assert factorial.__qualname__ == "factorial"
    assert factorial(0) == 1, "Base case should be executed"

    for n in range(1, 100):
        assert factorial(n) == _factorial(n)

    assert factorial(1_100), "This shouldn't raise a RecursionError"

    factorial_ = identity(identity(factorial))
    assert factorial_(1_100), "tailrec should work in a decorator chain"


def test_ping_pong():
    for i in range(1, 100):
        assert ping_pong(i) == "pong", "Should return 'pong'"

    assert ping_pong(100) is None, "Should return None"
