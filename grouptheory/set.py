class Set(frozenset):

    def __mul__(self, other):
        if not isinstance(other, Set):
            raise TypeError("Other parameter must be an instance of Set")
        return Set((x, y) for x in self for y in other)

    def get(self):
        if len(self) == 0:
            raise KeyError("Trying to fetch value from a empty set")
        for item in self:
            break
        return item