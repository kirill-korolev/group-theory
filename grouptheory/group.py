from grouptheory.set import Set
from grouptheory.operation import Operation


class Group:

    def __init__(self, group_set, op):

        if not isinstance(group_set, Set):
            raise TypeError("First parameter must be an instance of Set")

        if not isinstance(op, Operation):
            raise TypeError("Second parameter must be an instance of Operation")

        if op.src != group_set * group_set:
            raise ValueError("Operation source must be a Cartesian product of %s" % type(group_set))

        if op.dst != group_set:
            raise ValueError("Operation destination must be a %s" % type(group_set))

        if not Group.is_associative(group_set, op):
            raise ValueError("Group operation is not associative")

        self.id = Group.find_identity(group_set, op)

        if self.id is None:
            raise ValueError("Group set identity is missing")

        if not Group.has_invertibility(group_set, op, self.id):
            raise ValueError("Element %s doesn't have an inverse element" % x)

        self._set = group_set
        self._op = op
        self._abelian = Group.check_abelian(self._set, self._op)

    def __len__(self):
        return len(self._set)

    def group_set(self):
        return self._set

    def operation(self):
        return self._op

    def is_abelian(self):
        return self._abelian

    @staticmethod
    def find_identity(group_set, op):
        for x in group_set:
            found = True
            for y in group_set:
                if op((x, y)) != y:
                    found = False
                    continue
            if found:
                return x
        return None

    @staticmethod
    def is_associative(group_set, op):
        for a in group_set:
            for b in group_set:
                for c in group_set:
                    if not op((a, op((b, c)))) == op((op((a, b)), c)):
                        return False
        return True

    @staticmethod
    def has_invertibility(group_set, op, id):
        for x in group_set:
            if not any(op((x, y)) == id for y in group_set):
                return False
        return True

    @staticmethod
    def check_abelian(group_set, op):
        return all(op((x, y)) == op((y, x)) for x in group_set for y in group_set)