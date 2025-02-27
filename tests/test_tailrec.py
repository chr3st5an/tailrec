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

from tailrec import tailrec


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


def test_factorial():
    assert hasattr(factorial, "__name__")
    assert factorial.__qualname__ == "factorial"
    assert factorial(0) == 1, "Base case should be executed"

    for n in range(1, 100):
        assert factorial(n) == _factorial(n)

    assert factorial(1_100), "This shouldn't raise a RecursionError"
