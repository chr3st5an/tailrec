# tailrec

Provides a decorator `tailrec` which executes a tail recursive function iteratively

## Installation

```bash
pip install tailrec
```

## Usage

Decorate the target function with `tailrec`. The first argument of the function is a callable object representing a recursive call. Make sure to use this callable in combination with a `return` statement.

## Examples

```py
from tailrec import tailrec


@tailrec
def factorial(f, n: int, accum: int = 1) -> int:
    """Calculates n!"""
    if n == 0:
        return accum
    else:
        return f(n - 1, accum * n)


@tailrec
def fibonacci(f, n: int, current: int = 0, next_: int = 1) -> int:
    """Returns the n-th number of the fibonacci sequence"""
    if n == 0:
        return current
    else:
        return f(n - 1, next_, current + next_)


print(factorial(5))  # 120
print(factorial(1_100))  # 5343708488092637703...

print(fibonacci(5))  # 8
print(fibonacci(2_000))  # 42246963333923...
```
