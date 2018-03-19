from grouptheory.set import Set


class Operation:

    def __init__(self, src, dst, op):
        if not isinstance(src, Set):
            raise TypeError("Source set must be an instance of Set")
        if not isinstance(dst, Set):
            raise TypeError("Destination set must be an instance of Set")
        if not all(op(x) in dst for x in src):
            raise TypeError("Operation is defined outside of destination set")

        self.src = src
        self.dst = dst
        self.op = op

    def __call__(self, x):
        if x not in self.src:
            raise TypeError("Element x is not in source set")
        return self.op(x)

    def __eq__(self, other):
        if not isinstance(other, Operation):
            return False

        return id(self) == id(other) or (
            self.src == other.src and
            self.dst == other.dst and
            all(self(x) == other(x) for x in self.src)
        )

    def __ne__(self, other):
        return not (self == other)

    def image(self):
        return Set([self(x) for x in self.src])

    def is_surjective(self):
        return self.image() == Set(self.dst)

    def is_injective(self):
        return len(self.image()) == self.src

    def is_bijective(self):
        return self.is_surjective() and self.is_injective()

    def composition(self, other):
        if self.src != other.dst:
            raise ValueError("Inner operation destination doesn't match outer operation source")
        return Operation(other.src, self.dst, lambda x: self(other(x)))

    def init_with_domains(self, src, dst):
        return Operation(src, dst, self.op)

    @staticmethod
    def identity(group_set):
        if not isinstance(group_set, Set):
            raise TypeError("Parameter must be an instance of Set")
        return Operation(group_set, group_set, lambda x: x)