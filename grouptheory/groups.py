import itertools
from .set import Set
from .operation import Operation
from .group import Group


def Sn(n):
    S = Set(s for s in itertools.permutations(range(n)))
    op = Operation(S * S, S, lambda s: tuple(s[0][i] for i in s[1]))
    return Group(S, op)


def Zn(n):
    Z = Set(range(n))
    op = Operation(Z * Z, Z, lambda z: (z[0] + z[1]) % n)
    return Group(Z, op)