# tailrec

Provides a decorator `tailrec` which executes a tail recursive function iteratively

## Installation

```bash
pip install tailrec
```

## Usage

Decorate the target function with `tailrec`. The first argument of the function is a callable object representing a recursive call. Make sure to use this callable in combination with a `return` statement.

## Example

```py
from tailrec import tailrec


@tailrec
def factorial(f, n: int, accum: int = 1) -> int:
    if n > 0:
        return f(n - 1, accum * n)
    else:
        return accum


print(factorial(1_100))
```
