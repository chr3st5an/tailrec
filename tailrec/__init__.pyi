from typing import Callable, ParamSpec, TypeVar


P = ParamSpec('P')
R = TypeVar('R')


def tailrec(__func: Callable[P, R]) -> Callable[P, R]: ...
