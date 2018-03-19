class Set(frozenset):

    def __mul__(self, other):
        if not isinstance(other, Set):
            raise TypeError("Other parameter must be an instance of Set")
        return Set((x, y) for x in self for y in other)