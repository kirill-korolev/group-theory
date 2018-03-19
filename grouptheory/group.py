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

        id = Group.identity(group_set, op)

        if id is None:
            raise ValueError("Group set identity is missing")

        if not Group.has_invertibility(group_set, op, id):
            raise ValueError("Some element in group doesn't have an inverse")

        self.set = group_set
        self.op = op
        self.elems = Set(Element(g, self) for g in self.set)
        self.id = Element(id, self)
        self.is_abelian = Group.if_abelian(self.set, self.op)

    def __len__(self):
        return len(self.set)

    def __iter__(self):
        yield self.id

        for g in self.elems:
            if g != self.id:
                yield g

    def __contains__(self, item):
        return item in self.elems

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False

        return id(self) == id(other) or (
            self.set == other.set and self.op == other.op
        )

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        if not isinstance(other, Group):
            raise TypeError("Other is not an instance of Group")
        for a in self.elems:
            for b in self.elems:
                bi = self.inverse(b)
                if a * bi not in self.elems:
                    return False
        return self.set <= other.set and len(self.set) > 0

    def is_normal_subgroup(self, other):
        return self <= other and all(Set(h * g for h in self) == Set(g * h for h in self) for g in other)

    def inverse(self, x):
        if x not in self.elems:
            raise ValueError("%s doesn't belong to this set")
        for g in self:
            if x * g == self.id:
                return g
        return None

    def orbit(self, m, M):
        if not isinstance(M, Set):
            raise TypeError("M must be an instance of Set")
        if m not in M:
            raise ValueError("%s element doesn't belong to set")
        orb = Set()
        for g in self.set:
            gm = self.op((g, m))
            if M.issubset([gm]):
                orb = Set(orb.union([gm]))
        return orb

    def stabilizer(self, m, M):
        if not isinstance(M, Set):
            raise TypeError("M must be an instance of Set")
        if m not in M:
            raise ValueError("%s element doesn't belong to set")
        subset = Set()

        for g in self.set:
            if self.op((g, m)) == m:
                subset = Set(subset.union([g]))
        return subset

    def __mul__(self, other):
        if not isinstance(other, Group):
            raise TypeError("Other must be a Group")
        op = Operation((self.set * other.set) * (self.set * other.set), (self.set * other.set),
                       lambda x: (self.op((x[0][0], x[1][0])), self.op((x[0][1], x[1][1]))))
        return Group(self.set * other.set, op)

    def __str__(self):
        letters = "exyzabcd"
        if len(self) > len(letters):
            return "Can't print a Cayley table"

        to_letter = {}
        to_elem = {}
        for letter, elem in zip(letters, self):
            to_letter[elem] = letter
            to_elem[letter] = elem
        letters = letters[:len(self)]

        result = "\n".join("%s: %s" % (l, to_elem[l]) for l in letters) + "\n\n"

        def print_tables():
            nonlocal result
            nonlocal letters

            head_letters = "   | " + " | ".join(l for l in letters) + " |"
            head_values = "   | " + " | ".join(str(to_elem[l]) for l in letters) + " |"

            border = (len(self) + 1) * "---+" + "\t" + (len(self) + 1) * "---+" + "\n"
            result += head_letters + "\t" + head_values + "\n" + border
            result += border.join(" %s | " % l +
                                  " | ".join(to_letter[to_elem[l] * to_elem[l1]]
                                             for l1 in letters) + "\t\t" +
                                  " %s | " % to_elem[l] +
                                  " | ".join(str(to_elem[l] * to_elem[l1])
                                             for l1 in letters) +
                                  " | \n" for l in letters)
            result += border

        # def values_mode():
        #
        #     result += head + "\n" + border
        #     result += border.join(" %s | " % to_elem[l] +
        #                           " | ".join(str(to_elem[l] * to_elem[l1])
        #                                      for l1 in letters) +
        #                           " |\n" for l in letters)
        #     result += border

        print_tables()
        return result

    @staticmethod
    def identity(group_set, op):
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
    def if_abelian(group_set, op):
        return all(op((x, y)) == op((y, x)) for x in group_set for y in group_set)


class Element:

    def __init__(self, x, group):
        if not isinstance(group, Group):
            raise TypeError("group is not an instance of Group")
        if x not in group.set:
            raise ValueError("Element %s is not in group" % x)
        self.x = x
        self.group = group

    def __eq__(self, other):
        if not isinstance(other, Element):
            raise TypeError("Other element is not an instance of Element")
        return self.x == other.x

    def __ne__(self, other):
        return not (self == other)

    def __mul__(self, other):

        if not isinstance(other, Element):
            raise TypeError("Other must be an Element")

        try:
            return Element(self.group.op((self.x, other.x)), self.group)
        except TypeError:
            return other.__rmul__(self)

    def __rmul__(self, other):

        if not isinstance(other, Element):
            raise TypeError("Other must be an Element")

        return Element(self.group.op((other.x, self.x)), self.group)

    def __add__(self, other):
        if self.group.is_abelian:
            return self * other
        raise TypeError("%s is not an element of abelian group")

    def __hash__(self):
        return hash(self.x)

    def __str__(self):
        return str(self.x)